const puppeteer = require('puppeteer-core');
const fs = require('fs');
const http = require('http');

// Start a simple server to serve the model and image
const server = http.createServer((req, res) => {
  if (req.url === '/crop_model.tflite') {
    res.writeHead(200, {'Content-Type': 'application/octet-stream', 'Access-Control-Allow-Origin': '*'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\website\\public\\ml\\crop_model.tflite'));
  } else if (req.url === '/tflite.js') {
    res.writeHead(200, {'Content-Type': 'application/javascript', 'Access-Control-Allow-Origin': '*'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\website\\node_modules\\@tensorflow\\tfjs-tflite\\dist\\tf-tflite.min.js'));
  } else {
    res.writeHead(404);
    res.end();
  }
}).listen(9999);

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js' });
  await page.addScriptTag({ url: 'http://localhost:9999/tflite.js' });

  const imageBase64 = fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg').toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const pythonTensorRaw = JSON.parse(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_python_tensor.json').toString());

  const result = await page.evaluate(async (dataUrl, pyTensorData) => {
    tflite.setWasmPath('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/');
    const model = await tflite.loadTFLiteModel('http://localhost:9999/crop_model.tflite');
    
    // 1. JS Preprocessing (Current Code)
    const img = new Image();
    img.src = dataUrl;
    await new Promise(r => { img.onload = r; });
    
    let tensor = tf.browser.fromPixels(img);
    let tensorBilinear = tf.image.resizeBilinear(tensor, [224, 224]);
    let jsTensor = tf.cast(tensorBilinear, 'float32').div(255.0);
    const batchedJs = jsTensor.expandDims(0);

    // 2. Load Python Tensor (Nearest Neighbor)
    const pyFlat = new Float32Array(pyTensorData.full_tensor);
    const batchedPy = tf.tensor(pyFlat, [1, 224, 224, 3], 'float32');

    // 3. Inference
    const predJs = model.predict(batchedJs);
    const predPy = model.predict(batchedPy);

    const probsJs = Array.from(predJs.dataSync());
    const probsPy = Array.from(predPy.dataSync());

    return {
      js_first_100: Array.from(jsTensor.dataSync()).slice(0, 100),
      js_shape: jsTensor.shape,
      js_dtype: jsTensor.dtype,
      js_min: jsTensor.min().dataSync()[0],
      js_max: jsTensor.max().dataSync()[0],
      js_mean: jsTensor.mean().dataSync()[0],
      js_full_tensor: Array.from(jsTensor.dataSync()),
      probs_js: probsJs,
      probs_py: probsPy
    };
  }, dataUrl, pythonTensorRaw);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_js_results.json', JSON.stringify(result));
  console.log("JS inference and evaluation complete.");
  
  await browser.close();
  server.close();
})();
