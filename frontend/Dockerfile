# ── base: install deps ────────────────────────────────────────
FROM node:20-alpine AS base

WORKDIR /app

COPY package*.json ./
RUN npm ci

# ── dev: source mounted via compose volume, hot-reload ────────
FROM base AS dev

ENV NODE_ENV=development

CMD ["npm", "run", "dev"]

# ── builder: compile for production ───────────────────────────
FROM base AS builder

COPY . .
RUN npm run build

# ── prod: minimal runtime image ───────────────────────────────
FROM node:20-alpine AS prod

WORKDIR /app

ENV NODE_ENV=production

# Only copy what next start needs
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
