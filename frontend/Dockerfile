# Use Node.js 22 Alpine as base image for smaller size
FROM node:22-alpine AS base

# Install pnpm via corepack
RUN npm install -g corepack@latest
RUN corepack use pnpm@latest-10

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source code
COPY . .

# Build the application
RUN pnpm run build

# Production stage
FROM node:22-alpine AS production

# Install curl for health checks
RUN apk add --no-cache curl

# Install pnpm via corepack
RUN npm install -g corepack@latest
RUN corepack use pnpm@latest-10

# Set working directory
WORKDIR /app

# Copy built application from build stage
COPY --from=base /app/.output ./.output
COPY --from=base /app/package.json ./
COPY --from=base /app/pnpm-lock.yaml ./

# Install only production dependencies
RUN pnpm install --prod --frozen-lockfile

# Create non-root user for security
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nuxt -u 1001

# Change ownership of app directory
RUN chown -R nuxt:nodejs /app
USER nuxt

# Expose port
EXPOSE 3000

# Set environment variables
ENV NODE_ENV=production
ENV PORT=3000


# Start the application
CMD ["pnpm", "run", "preview"]
