module.exports = {
    extends: ["eslint:recommended", "prettier"],
    root: true,
    env: {
        es6: "true",
        browser: true,
        node: true,
        jest: true,
    },
    globals: {
        "jQuery": true,
        "Faceted": true,
        "FacetedEdit": true,
        "FacetedTree": true
    },
    parser: "@babel/eslint-parser",
    ignorePatterns: [
        "cache/",
        "coverage/",
        "dist/",
        "node_modules/",
        "stats.json",
        "style/",
    ],
    rules: {
        "no-debugger": 1,
        "no-duplicate-imports": 1,
        // Do keep due avoid unintended consequences.
        "no-alert": 0,
        "no-control-regex": 0,
        "no-self-assign": 0,
        "no-useless-escape": 0,
    },
};
