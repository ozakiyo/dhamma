const path = require('path');

/**
 * ダンマ指針アプリ専用 pm2 設定（ozakiyo/dhamma リポジトリ用）
 *
 * サーバー上（/opt/dhamma がこのリポの clone）:
 *   pm2 start deploy/ecosystem.dhamma.config.cjs
 *   pm2 restart dhamma
 */
module.exports = {
  apps: [
    {
      name: 'dhamma',
      cwd: path.join(__dirname, '..'),
      script: 'deploy/dhamma-serve.mjs',
      interpreter: 'node',
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      out_file: path.join(__dirname, '../logs/dhamma-out.log'),
      error_file: path.join(__dirname, '../logs/dhamma-err.log'),
      merge_logs: true,
      env: {
        NODE_ENV: 'production',
        DHAMMA_PORT: '3053',
        DHAMMA_ROOT: '/opt/dhamma',
      },
    },
  ],
};
