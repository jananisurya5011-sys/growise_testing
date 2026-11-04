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

    const blob = await fetch(dataUrl).then(r => r.blob());
    const file = new File([blob], 'test.jpg', { type: 'image/jpeg' });
    
    async function runInference(reqId) {
      log(`\n============================`);
      log(`REQUEST: ${reqId}`);
      log(`============================`);
      
      const t0 = performance.now();
      
      // 1. File Selected
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] File selected`);
      
      // 2. Blob URL
      const url = URL.createObjectURL(file);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Blob URL created`);
      
      // DOM Mount
      const img = document.createElement('img');
      img.src = url;
      document.body.appendChild(img);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Image component mounts`);
      
      // Decode
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Image decode starts`);
      try {
        await img.decode();
        log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Image decode ends`);
      } catch(e) {
        log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Image decode ERROR`);
      }
      
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] image.complete: ${img.complete}`);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] image.naturalWidth: ${img.naturalWidth}`);
      
      // createImageBitmap
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] createImageBitmap() start`);
      const bitmap = await createImageBitmap(file);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] createImageBitmap() end. Width: ${bitmap.width}`);
      
      // Canvas Draw
      const canvas = document.createElement('canvas');
      canvas.width = 224; canvas.height = 224;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, 224, 224);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Canvas drawImage()`);
      
      // Canvas pixels
      const pixels = Array.from(ctx.getImageData(0,0,224,224).data).slice(0, 10);
      const pixelSum = Array.from(ctx.getImageData(0,0,224,224).data).reduce((a,b)=>a+b,0);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Canvas first 10 pixels: ${pixels.join(',')}`);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] Canvas checksum: ${pixelSum}`);
      
      // fromPixels (DOM)
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] fromPixels(img) starts`);
      const tensorImg = tf.browser.fromPixels(img);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] fromPixels(img) ends. Mean: ${tensorImg.mean().dataSync()[0]}`);
      
      // fromPixels (Bitmap)
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] fromPixels(bitmap) starts`);
      const tensorBitmap = tf.browser.fromPixels(bitmap);
      log(`[${(performance.now() - t0).toFixed(2)}][${reqId}] fromPixels(bitmap) ends. Mean: ${tensorBitmap.mean().dataSync()[0]}`);
      
      document.body.removeChild(img);
      return { pixelSum, imgMean: tensorImg.mean().dataSync()[0], bmpMean: tensorBitmap.mean().dataSync()[0] };
    }

    await tf.ready();
    tf.env().set('WEBGL_PACK', false); // Force robust WebGL extraction

    const res1 = await runInference('REQ_1_FIRST_CLICK');
    const res2 = await runInference('REQ_2_SECOND_CLICK');
    
    log(`\n\n=== COMPARISON TABLE ===`);
    log(`Metric | FIRST CLICK | SECOND CLICK | MATCH?`);
    log(`Canvas Checksum | ${res1.pixelSum} | ${res2.pixelSum} | ${res1.pixelSum === res2.pixelSum}`);
    log(`fromPixels(DOM) Mean | ${res1.imgMean} | ${res2.imgMean} | ${res1.imgMean === res2.imgMean}`);
    log(`fromPixels(Bitmap) Mean | ${res1.bmpMean} | ${res2.bmpMean} | ${res1.bmpMean === res2.bmpMean}`);
    
    return logs.join('\n');
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\forensic_bitmap_report.txt', result);
  return "Done";
})();
