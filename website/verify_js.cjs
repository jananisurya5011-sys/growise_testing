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
  const imageBase64 = fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\test_image.png').toString('base64');
  const dataUrl = `data:image/png;base64,${imageBase64}`;

  const result = await page.evaluate(async (dataUrl) => {
    const img = new Image();
    img.src = dataUrl;
    await new Promise(r => { img.onload = r; });
    
    // Exact pipeline from tfModelLoader.js
    let tensor = tf.browser.fromPixels(img);
    let tensorBilinear = tf.image.resizeBilinear(tensor, [224, 224]);
    let normalizedBilinear = tf.cast(tensorBilinear, 'float32').div(255.0);
    
    // Also compute Nearest Neighbor for comparison
    let tensorNearest = tf.image.resizeNearestNeighbor(tensor, [224, 224]);
    let normalizedNearest = tf.cast(tensorNearest, 'float32').div(255.0);

    const flatBilinear = Array.from(normalizedBilinear.dataSync()).slice(0, 100);
    const flatNearest = Array.from(normalizedNearest.dataSync()).slice(0, 100);

    return {
      js_bilinear_first_100: flatBilinear,
      js_nearest_first_100: flatNearest,
      shape: normalizedBilinear.shape,
      dtype: normalizedBilinear.dtype,
      min: normalizedBilinear.min().dataSync()[0],
      max: normalizedBilinear.max().dataSync()[0],
      mean: normalizedBilinear.mean().dataSync()[0]
    };
  }, dataUrl);
  
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\js_results.json', JSON.stringify(result, null, 2));
  console.log("JS preprocessing complete. Results saved.");
  
  await browser.close();
})();
