const http = require('http');
const fs = require('fs');
const path = require('path');
const qs = require('querystring');

const port = 8080;

const server = http.createServer((req, res) => {
  if (req.method === 'GET') {
    // GETリクエストの処理
    if (req.url === '/') {
      // ルートパスへのGETリクエストに対してデータを返す
      const indexPath = path.join(__dirname, 'public.html');
      fs.readFile(indexPath, 'utf8', (err, data) => {
        if (err) {
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Internal Server Error');
        } else {
          res.writeHead(200, { 'Content-Type': 'text/html' });
          res.end(data);
        }
      });
    } else {
      // その他のGETリクエストに対して静的ファイルを返す
      const filePath = path.join(__dirname, req.url);
      fs.readFile(filePath, (err, data) => {
        if (err) {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('Not Found');
        } else {
          // ファイルの拡張子に基づいてContent-Typeを設定
          const extname = path.extname(filePath);
          let contentType = 'text/plain';
          switch (extname) {
            case '.html':
              contentType = 'text/html';
              break;
            case '.css':
              contentType = 'text/css';
              break;
            case '.png':
              contentType = 'image/png';
              break;
            // 他のファイルタイプも追加可能
          }

          res.writeHead(200, { 'Content-Type': contentType });
          res.end(data);
        }
      });
    }
  } else if (req.method === 'POST' && req.url === '/submit') {
    // POSTリクエストの処理
    let body = '';
    req.on('data', (chunk) => {
      body += chunk.toString();
    });

    req.on('end', () => {
      const postData = qs.parse(body);
      const { username, password } = postData;
      const data = `${username},${password}\n`;

      fs.appendFile('user_data.csv', data, (err) => {
        if (err) {
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Internal Server Error');
        } else {
          res.writeHead(200, { 'Content-Type': 'text/plain' });
          res.end('Data successfully submitted');
        }
      });
    });
  } else {
    // その他のリクエストには404を返す
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not Found');
  }
});

server.listen(port, () => {
  console.log(`サーバーがポート ${port} で起動しました。`);
});

