# OtakuShelf Frontend

This is the frontend for OtakuShelf, a web application that allows users to search for anime and create a watch list. The frontend is built using Nuxt.js and communicates with the backend API to provide a seamless user experience.

## Features

- Search for anime by title, genre, or other criteria
- Create and manage a watch list for tracking anime progress
- User authentication and profile management
- Responsive design for optimal viewing on various devices

## Technologies Used

- Nuxt.js (Progressive Vue.js Framework)
- Nuxt UI (UI component library for Nuxt.js based on Tailwind CSS)

## Getting Started

### Prerequisites

- Node.js (version 22 or higher)
- pnpm (Package Manager)

### Installation and Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
    cd OtakuShelf/frontend
   ```

2. Install dependencies using pnpm:

   ```bash
   pnpm install
   ```

3. Create a `.env` file in the `frontend` directory and add the necessary environment variables. You can refer to the `.env.example` file for guidance.

### Running the Application

#### Development Server

Start the development server:

```bash
pnpm run dev
```

The application will be running at `http://localhost:3000`.

#### Production Build

To create a production build of the application, run:

```bash
pnpm run build
```

You can then start the production server with:

```bash
pnpm run start
```

## Testing

To run tests, use the following command:

```bash
pnpm run test
```

This will execute the test suite and provide feedback on the test results.

## Linting

The project uses ESLint for linting the codebase.

To check for linting issues, run:

```bash
pnpm run lint
```

This will analyze the codebase for any linting errors or warnings.
To automatically fix linting issues, run:

```bash
pnpm run lint:fix
```

This will attempt to fix any linting issues that can be automatically resolved.
