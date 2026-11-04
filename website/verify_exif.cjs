const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new'
  });
  const page = await browser.newPage();
  
  await page.addScriptTag({ url: 'https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js' });

  // Read the image as base64 to pass it into the page
  const imageBase64 = fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\test_exif.jpg').toString('base64');
  const dataUrl = `data:image/jpeg;base64,${imageBase64}`;

  const result = await page.evaluate(async (dataUrl) => {
    const img = new Image();
    img.src = dataUrl;
    await new Promise(r => { img.onload = r; });
    
    // Exact pipeline from tfModelLoader.js
    let tensor = tf.browser.fromPixels(img);

    const firstPixel = Array.from(tensor.slice([0, 0, 0], [1, 1, 3]).dataSync());
    const shape = tensor.shape;

    return {
      js_shape: shape,
      js_first_pixel: firstPixel
    };
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\js_exif_results.json', JSON.stringify(result, null, 2));
  console.log("JS EXIF test complete. Results saved.");
  
  await browser.close();
})();
