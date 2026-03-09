/// <reference types="vitest/globals" />
import "@testing-library/jest-dom";

// Silence fetch calls made by components (e.g. KanbanBoard auto-save) in jsdom,
// which has no base URL and cannot resolve relative URLs like /api/board.
global.fetch = vi.fn(() => Promise.resolve(new Response(null, { status: 200 })));
