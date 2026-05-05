/**
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2026 Univention GmbH
 */

const js = require("@eslint/js");
const globals = require("globals");

module.exports = [
  {
    ignores: ["public/fingerprintjs/v3.js"]
  },
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: "latest",
      globals: {
        ...globals.node,
      }
    },
    rules: {
      "no-unused-vars": "warn",
      "indent": ["error", 2],
      "linebreak-style": ["error", "unix"],
      "quotes": ["error", "double"],
      "semi": ["error", "always"]
    }
  }
];
