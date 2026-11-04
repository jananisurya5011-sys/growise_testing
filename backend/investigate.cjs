const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js' });
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/tf-tflite.min.js' });

  const imagePath = 'C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg';
  const imageBase64 = fs.readFileSync(imagePath).toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const result = await page.evaluate(async (dataUrl) => {
    // We will simulate the exact failure scenario
    const logs = [];
    const log = (msg) => logs.push(msg);

    log("=== STEP 1: Flow Traced ===");
    log("File selection -> ObjectURL -> rendering -> button click -> tfModelLoader.predict");

    // Load Model
    tflite.setWasmPath('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/');
    const model = await tflite.loadTFLiteModel('/ml/crop_model.tflite').catch(() => null);
    // Since we are in an isolated page without the server, we will simulate the tensor generation
    // to prove the input pipeline bug. The model isn't strictly necessary to prove tf.browser.fromPixels fails.
    
    // Create image
    const img = new Image();
    img.src = dataUrl;

    const analyzeImage = (clickName) => {
      log(`\n=== STEP 2: Verify Image Valid (${clickName}) ===`);
      log(`image.complete: ${img.complete}`);
      log(`image.naturalWidth: ${img.naturalWidth}`);
      log(`image.naturalHeight: ${img.naturalHeight}`);
      log(`image.width: ${img.width}`);
      log(`image.height: ${img.height}`);

      let tensor;
      try {
        tensor = tf.browser.fromPixels(img);
      } catch (e) {
        log(`Error in fromPixels: ${e.message}`);
        tensor = tf.zeros([0, 0, 3]);
      }

      log(`\n=== STEP 3: Tensor after fromPixels (${clickName}) ===`);
      log(`shape: ${tensor.shape}`);
      log(`dtype: ${tensor.dtype}`);
      try {
        log(`minimum: ${tensor.min().dataSync()[0]}`);
        log(`maximum: ${tensor.max().dataSync()[0]}`);
        log(`mean: ${tensor.mean().dataSync()[0]}`);
        log(`first 20: ${Array.from(tensor.dataSync()).slice(0, 20)}`);
      } catch(e) {}

      let resized;
      if (tensor.shape[0] > 0) {
        resized = tf.image.resizeNearestNeighbor(tensor, [224, 224], false, true);
      } else {
        resized = tf.zeros([224, 224, 3]);
      }

      log(`\n=== STEP 4: Tensor after resize (${clickName}) ===`);
      log(`shape: ${resized.shape}`);
      log(`minimum: ${resized.min().dataSync()[0]}`);
      log(`maximum: ${resized.max().dataSync()[0]}`);
      log(`mean: ${resized.mean().dataSync()[0]}`);

      const normalized = resized.cast('float32').div(255.0);
      log(`\n=== STEP 5: Tensor after normalization (${clickName}) ===`);
      log(`minimum: ${normalized.min().dataSync()[0]}`);
      log(`maximum: ${normalized.max().dataSync()[0]}`);
      log(`mean: ${normalized.mean().dataSync()[0]}`);

      return normalized;
    };

    // FIRST CLICK (Immediate)
    log("\n--- FIRST CLICK (Simulated Immediate Click) ---");
    const t1 = analyzeImage("First Click");
    
    // Wait for image to fully load natively
    await img.decode();
    
    // SECOND CLICK (After loaded)
    log("\n--- SECOND CLICK (Simulated After Load) ---");
    const t2 = analyzeImage("Second Click");

    log(`\n=== STEP 6: Backend ===`);
    log(`tf.getBackend(): ${tf.getBackend()}`);

    return logs.join('\n');
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\investigate_report.txt', result);
  console.log("Investigation report saved.");
  
  await browser.close();
})();
