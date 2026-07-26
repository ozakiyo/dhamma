FROM node:22-alpine

WORKDIR /app

EXPOSE 3053

CMD ["node", "deploy/dhamma-serve.mjs"]
