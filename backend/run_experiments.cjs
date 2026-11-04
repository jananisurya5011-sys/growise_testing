const puppeteer = require('puppeteer-core');
const fs = require('fs');
const http = require('http');

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.url === '/') {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(`
      <html>
        <head>
          <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js"></script>
          <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/tf-tflite.min.js"></script>
        </head>
        <body>
          <script>
            async function runTests() {
              tflite.setWasmPath('https://cdn.jsdelivr.net/npm/@tensorflow/tfjs-tflite@0.0.1-alpha.10/dist/');
              const model = await tflite.loadTFLiteModel('/model.tflite');
              
              const pyBicubic = await fetch('/pyBicubic.json').then(r => r.json());
              const pyNearest = await fetch('/pyNearest.json').then(r => r.json());
              const jsBilinear = await fetch('/jsBilinear.json').then(r => r.json());
              const jsNearest = await fetch('/jsNearest.json').then(r => r.json());

              const tPyBicubic = tf.tensor(new Float32Array(pyBicubic.python_bicubic_full), [1, 224, 224, 3], 'float32');
              const tPyNearest = tf.tensor(new Float32Array(pyNearest.full_tensor), [1, 224, 224, 3], 'float32');
              const tJsBilinear = tf.tensor(new Float32Array(jsBilinear.js_full_tensor), [1, 224, 224, 3], 'float32');
              const tJsNearest = tf.tensor(new Float32Array(jsNearest.js_full_tensor), [1, 224, 224, 3], 'float32');
              
              const pA = Array.from(model.predict(tPyBicubic).dataSync());
              const pC = Array.from(model.predict(tPyNearest).dataSync());
              const pD = Array.from(model.predict(tJsBilinear).dataSync());
              const pE = Array.from(model.predict(tJsNearest).dataSync());

              window.results = { pA, pC, pD, pE };
              document.body.innerHTML += '<h1>DONE</h1>';
            }
            runTests().catch(e => {
                window.results = { error: e.message };
                document.body.innerHTML += '<h1>ERROR</h1>';
            });
          </script>
        </body>
      </html>
    `);
  } else if (req.url === '/model.tflite') {
    res.writeHead(200, {'Content-Type': 'application/octet-stream'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\website\\public\\ml\\crop_model.tflite'));
  } else if (req.url === '/pyBicubic.json') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_python_bicubic.json'));
  } else if (req.url === '/pyNearest.json') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_python_tensor.json'));
  } else if (req.url === '/jsBilinear.json') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_js_results.json'));
  } else if (req.url === '/jsNearest.json') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(fs.readFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\dis2_js_nearest.json'));
  } else {
    res.writeHead(404); res.end();
  }
}).listen(9999);

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  await page.goto('http://localhost:9999/');
  await page.waitForFunction('window.results !== undefined', {timeout: 30000});
  
  const result = await page.evaluate(() => window.results);
  fs.writeFileSync('C:\\Projects\\GroWise_Fullstack\\GroWise\\backend\\experiment_results.json', JSON.stringify(result, null, 2));
  console.log("Experiments complete.");
  
  await browser.close();
  server.close();
})();
