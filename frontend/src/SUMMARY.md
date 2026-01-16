# frontend/src/

Frontend application source code.

## Purpose
Root source directory for the React + TypeScript application. Contains entry points, root component, and organized subdirectories for components, state, services, and types.

## Contents

### Subdirectories

- **components/** - React UI components organized by feature
- **store/** - Zustand state management
- **services/** - API client for backend communication
- **types/** - TypeScript type definitions
- **assets/** - Static assets (images, icons)

### Files

- **main.tsx** - Application entry point that mounts React app to DOM
- **App.tsx** - Root component that renders GameBoard
- **App.css** - Styling for App component
- **index.css** - Global styles and Tailwind directives

### Functions in main.tsx

- **createRoot()** - React 18 API to create root renderer

### Functions in App.tsx

- **App()** - Root component function that returns GameBoard component

### Classes
None
