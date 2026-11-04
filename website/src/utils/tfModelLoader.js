import * as tf from '@tensorflow/tfjs';
import * as tflite from '@tensorflow/tfjs-tflite';

class TFModelLoader {
  constructor() {
    this.model = null;
    this.labels = [];
    this.initPromise = null;
  }

  initialize() {
    console.log(`[${performance.now().toFixed(2)}] tfModelLoader.initialize() START`);
    if (this.model && this.labels.length > 0) return Promise.resolve();
    if (this.initPromise) return this.initPromise;

    this.initPromise = (async () => {
      try {
        tflite.setWasmPath('/tflite/');
        this.model = await tflite.loadTFLiteModel('/ml/crop_model.tflite');
        const response = await fetch('/ml/labels.txt');
        const text = await response.text();
        this.labels = text.split('\n').map(l => l.trim()).filter(l => l.length > 0);
        await tf.ready();
        
        tf.tidy(() => {
          const dummyTensor = tf.zeros([1, 224, 224, 3]);
          const dummyPrediction = this.model.predict(dummyTensor);
          dummyPrediction.dataSync(); 
        });
        
        console.log(`[${performance.now().toFixed(2)}] tfModelLoader.initialize() END (Success)`);
      } catch (err) {
        console.error('Failed to load TFLite model or labels:', err);
        this.initPromise = null;
        throw err;
      }
    })();
    
    return this.initPromise;
  }

  async predict(fileObj, reqId = 'UNKNOWN_REQ') {
    console.log(`[${performance.now().toFixed(2)}] tfModelLoader.predict() START [ReqID: ${reqId}]`);
    if (!this.model || this.labels.length === 0) await this.initialize();
    if (!this.model) throw new Error("Model failed to load");

    let bitmap = null;
    try {
      bitmap = await createImageBitmap(fileObj);
    } catch (err) {
      console.error("createImageBitmap failed:", err);
      // Fallback: draw file to canvas if createImageBitmap is completely unsupported
      bitmap = await new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = () => {
          const canvas = document.createElement('canvas');
          canvas.width = img.width;
          canvas.height = img.height;
          const ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0);
          resolve(canvas);
        };
        img.onerror = reject;
        img.src = URL.createObjectURL(fileObj);
      });
    }

    const result = tf.tidy(() => {
      let tensor;
      try {
        tensor = tf.browser.fromPixels(bitmap);
      } catch (e) {
        console.log(`[${performance.now().toFixed(2)}] tf.browser.fromPixels failed [ReqID: ${reqId}]`);
        tensor = tf.zeros([0, 0, 3]);
      }
      
      let resized;
      if (tensor.shape[0] > 0) {
        resized = tf.image.resizeNearestNeighbor(tensor, [224, 224], false, true);
      } else {
        resized = tf.zeros([224, 224, 3]);
      }
      
      // Share of leaf-coloured pixels (green to yellow, reasonably saturated) used to reject non-plant photos
      const pixels = resized.dataSync();
      let leafPixels = 0;
      for (let p = 0; p < pixels.length; p += 3) {
        const r = pixels[p], g = pixels[p + 1], b = pixels[p + 2];
        const max = Math.max(r, g, b);
        const delta = max - Math.min(r, g, b);
        if (max < 40 || delta / max < 0.2) continue;
        if (max === g || (max === r && (g - b) / delta >= 0.58)) leafPixels++;
      }
      const leafRatio = leafPixels / (pixels.length / 3);

      const normalized = tf.cast(resized, 'float32').div(255.0);
      const batched = normalized.expandDims(0);
      
      console.log(`[${performance.now().toFixed(2)}] model.predict() START [ReqID: ${reqId}]`);
      const prediction = this.model.predict(batched);
      console.log(`[${performance.now().toFixed(2)}] model.predict() END [ReqID: ${reqId}]`);
      
      const probabilities = prediction.dataSync();
      
      let maxIndex = 0;
      let maxConfidence = 0;
      for (let i = 0; i < probabilities.length; i++) {
        if (probabilities[i] > maxConfidence) {
          maxConfidence = probabilities[i];
          maxIndex = i;
        }
      }

      const predictedLabel = this.labels[maxIndex] || "Unknown";
      
      console.log(`[${performance.now().toFixed(2)}] tfModelLoader.predict() END [ReqID: ${reqId}] | Disease: ${predictedLabel} | Confidence: ${maxConfidence} | LeafRatio: ${leafRatio.toFixed(3)}`);

      return {
        disease: predictedLabel,
        confidence: maxConfidence,
        leafRatio
      };
    });

    // Cleanup the bitmap to prevent memory leaks
    if (bitmap && typeof bitmap.close === 'function') {
      bitmap.close();
    }

    return result;
  }
}

const tfModelLoader = new TFModelLoader();
export default tfModelLoader;
