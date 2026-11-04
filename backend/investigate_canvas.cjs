const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js' });

  const imagePath = 'C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\uploads\\crop\\dis2.jpg';
  const imageBase64 = fs.readFileSync(imagePath).toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const result = await page.evaluate(async (dataUrl) => {
    const logs = [];
    const log = (msg) => logs.push(msg);

    // Track if DOM node changes
    let originalImgRef = null;
    let originalSrc = null;

    // Simulate file upload -> Blob URL creation
    const blob = await fetch(dataUrl).then(r => r.blob());
    const previewUrl = URL.createObjectURL(blob);
    
    // Simulate React render
    const img = document.createElement('img');
    img.id = 'diagnosis-upload-preview';
    img.src = previewUrl;
    document.body.appendChild(img);
    
    originalImgRef = img;
    originalSrc = img.src;

    log("--- FIRST CLICK (Simulated Immediate Click) ---");
    
    const currentImgRef = document.getElementById('diagnosis-upload-preview');
    log(`Does imageElement.src change between file selection and prediction? ${originalSrc !== currentImgRef.src}`);
    log(`Does the <img> DOM node get replaced? ${originalImgRef !== currentImgRef}`);
    log(`Is imageRef.current the same object before and during prediction? ${originalImgRef === currentImgRef}`);

    // Draw to Canvas
    const canvas = document.createElement('canvas');
    canvas.width = 224;
    canvas.height = 224;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    
    // Attempt to draw the image in its current (un-decoded) state
    try {
      ctx.drawImage(img, 0, 0, 224, 224);
      log("Canvas drawImage succeeded (no exception thrown)");
    } catch (e) {
      log(`Canvas drawImage exception: ${e.name} - ${e.message}`);
    }

    // Read Raw Canvas Pixels
    const imageData = ctx.getImageData(0, 0, 224, 224);
    const pixels = Array.from(imageData.data).slice(0, 100);
    log(`First 100 RGBA pixels from canvas:`);
    log(pixels.join(','));

    // Check if canvas is purely transparent/black
    const isBlank = pixels.every(p => p === 0);
    log(`Is canvas completely empty/transparent? ${isBlank}`);

    // Read into Tensor
    let tensor;
    try {
      tensor = tf.browser.fromPixels(canvas);
      log(`Tensor extracted successfully. Mean: ${tensor.mean().dataSync()[0]}`);
    } catch (e) {
      log(`tf.browser.fromPixels exception: ${e.name} - ${e.message}`);
    }

    log("\n--- SECOND CLICK (Simulated After Load) ---");
    await img.decode();
    
    ctx.drawImage(img, 0, 0, 224, 224);
    const imageData2 = ctx.getImageData(0, 0, 224, 224);
    const pixels2 = Array.from(imageData2.data).slice(0, 100);
    log(`First 100 RGBA pixels from canvas after load:`);
    log(pixels2.join(','));
    
    const tensor2 = tf.browser.fromPixels(canvas);
    log(`Tensor extracted successfully. Mean: ${tensor2.mean().dataSync()[0]}`);

    return logs.join('\n');
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\canvas_investigation.txt', result);
  return "Investigation complete.";
})();
