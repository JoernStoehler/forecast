// ESLint v9+ flat config bridging our existing setup
import tseslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";

export default [
  // Ignore build output
  { ignores: ["dist/**"] },
  {
    files: ["**/*.{ts,tsx,js,jsx}"]
    ,languageOptions: {
      parser: tsParser,
      ecmaVersion: "latest",
      sourceType: "module",
    },
    plugins: {
      "@typescript-eslint": tseslint,
    },
    // Start with @typescript-eslint recommended rules; expand as needed
    rules: {
      ...tseslint.configs.recommended.rules,
    },
  },
];

