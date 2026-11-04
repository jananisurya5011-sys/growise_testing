import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../../utils/apiClient';
import { useAuth } from '../../contexts/AuthContext';
import { ArrowLeft, AlertTriangle, CheckCircle } from 'lucide-react';
import tfModelLoader from '../../utils/tfModelLoader';
import { normalizeLabel, getCropFromLabel } from '../../utils/cropLabels';

import DiagnosisUpload from '../diagnosis/DiagnosisUpload';
import DiagnosisLoader from '../diagnosis/DiagnosisLoader';
import DiagnosisResultCard from '../diagnosis/DiagnosisResultCard';
import notify from '../../services/NotificationService';


const OfflineCropDoctor = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [errorAlert, setErrorAlert] = useState(null);
  const [isSaving, setIsSaving] = useState(false);
  const [metadata, setMetadata] = useState({});
  const [modelReady, setModelReady] = useState(false);

  useEffect(() => {
    let mounted = true;
    const initModel = async () => {
      try {
        await tfModelLoader.initialize();
        if (mounted) setModelReady(true);
      } catch (err) {
        console.error("Failed to initialize model", err);
      }
    };
    initModel();

    fetch('/ml/disease_metadata.json')
      .then(res => res.json())
      .then(data => { if (mounted) setMetadata(data); })
      .catch(err => console.error("Failed to load metadata", err));
      
    return () => { mounted = false; };
  }, []);

  const reqCounter = React.useRef(0);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);
    setResult(null);
    setErrorAlert(null);
  };

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  const handleDiagnose = async () => {
    reqCounter.current += 1;
    const currentReqId = `REQ_${reqCounter.current}`;
    
    if (!selectedFile || !modelReady) {
      return;
    }
    
    setIsAnalyzing(true);
    setErrorAlert(null);
    setResult(null);
    
    try {
      const startTime = Date.now();
      const prediction = await tfModelLoader.predict(selectedFile, currentReqId);
      const predictionTime = Date.now() - startTime;
      
      // Class 38 ("Unknown") is the model's non-plant class; low confidence or few leaf-coloured pixels also mean no leaf
      if (prediction.disease === 'Unknown' || prediction.confidence < 0.6 || prediction.leafRatio < 0.15) {
        setErrorAlert("This doesn't look like a plant leaf. Please upload a clear photo of a single leaf.");
      } else {
        // Match metadata keys to model labels regardless of underscores/punctuation
        const metaKey = Object.keys(metadata).find(k => normalizeLabel(k) === normalizeLabel(prediction.disease));
        const meta = metadata[metaKey] || {
          symptoms: ["Information unavailable"],
          causes: ["Information unavailable"],
          organicTreatment: ["Consult your local agriculture officer"],
          chemicalTreatment: ["Consult your local agriculture officer"],
          prevention: ["Information unavailable"]
        };

        const formattedDisease = prediction.disease.replace(/_+/g, ' ').replace(/\s+/g, ' ').trim();

        setResult({
          disease: formattedDisease,
          cropName: getCropFromLabel(prediction.disease),
          confidence: prediction.confidence,
          remedy: meta.organicTreatment.join(', ') + '\n\nChemical: ' + meta.chemicalTreatment.join(', '),
          predictionTime,
          modelVersion: 'TFLite WebGL v1.0'
        });
      }
    } catch (error) {
      console.error(error);
      setErrorAlert("Inference engine failed to run on this device.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSave = async () => {
    if (!result || !user?.email || !selectedFile) return;
    setIsSaving(true);
    
    const formData = new FormData();
    formData.append('email', user.email);
    formData.append('disease', result.disease);
    formData.append('remedy', result.remedy);
    formData.append('confidence', result.confidence);
    formData.append('diagnosisType', 'offline');
    formData.append('language', 'en');
    
    // Store additional metadata
    const details = {
      cropName: result.cropName || 'Unknown',
      predictionTimeMs: result.predictionTime,
      modelVersion: result.modelVersion
    };
    formData.append('details', JSON.stringify(details));
    
    formData.append('file', selectedFile); // The actual physical file

    try {
      const { data } = await apiClient.post('/api/crop-doctor/save-diagnosis', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      if (data.success) {
        notify.success("Saved to your Diagnostic History!");
        navigate('/home/farmer');
      } else {
        notify.error("Failed to save.");
      }
    } catch (error) {
      console.error(error);
      notify.error("Network error: failed to save diagnosis.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
      {/* Premium Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button onClick={() => navigate('/home/farmer')} style={{ background: '#fff', border: '1px solid #eee', width: '44px', height: '44px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.05)' }}>
            <ArrowLeft size={20} color="#333" />
          </button>
          <div>
            <h1 style={{ margin: 0, fontSize: '26px', fontWeight: 800, color: '#d9534f', letterSpacing: '-0.5px' }}>Offline Crop Doctor</h1>
            <p style={{ margin: 0, fontSize: '14px', color: '#666', fontWeight: 500 }}>Secure, instant local AI diagnosis.</p>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
        
        {/* Scanner Column */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          
          <DiagnosisUpload 
            onFileSelect={handleFileSelect}
            previewUrl={previewUrl}
            isAnalyzing={isAnalyzing}
          />
          
          <DiagnosisLoader 
            isAnalyzing={isAnalyzing}
            onClick={handleDiagnose}
            disabled={!selectedFile || isAnalyzing || !modelReady}
            text={!modelReady ? "Loading AI Model..." : "Analyze Leaf Offline"}
            analyzingText="Running Core Accelerator..."
          />

          {!result && !errorAlert && (
            <div style={{ backgroundColor: '#ecfdf5', borderRadius: '16px', padding: '16px', display: 'flex', alignItems: 'center', gap: '16px', border: '1px solid #a7f3d0' }}>
              <CheckCircle size={28} color="#059669" />
              <div>
                <h4 style={{ margin: 0, color: '#059669', fontSize: '15px', fontWeight: 800 }}>100% Offline Core Active</h4>
                <p style={{ margin: '4px 0 0 0', color: '#047857', fontSize: '13px' }}>Instant predictions powered by local TensorFlow WebGL acceleration.</p>
              </div>
            </div>
          )}

          {errorAlert && (
            <div style={{ backgroundColor: '#fef2f2', borderRadius: '16px', padding: '16px', display: 'flex', alignItems: 'center', gap: '16px', border: '1px solid #fecaca' }}>
              <AlertTriangle size={28} color="#dc2626" />
              <p style={{ margin: 0, color: '#dc2626', fontSize: '14px', fontWeight: 700 }}>{errorAlert}</p>
            </div>
          )}
        </div>

        {/* Results Column */}
        <DiagnosisResultCard 
          result={result}
          diagnosisType="offline"
          onSave={handleSave}
          isSaving={isSaving}
        />
        
      </div>
    </div>
  );
};

export default OfflineCropDoctor;
