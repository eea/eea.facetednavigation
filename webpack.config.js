process.traceDeprecation = true;
const path = require("path");

module.exports = [
    {
        entry: './resources/plugins.js',
        // optimization: {
        //     minimize: false
        // },
        output: {
            path: path.resolve(__dirname, 'eea/facetednavigation/browser/static'),
            filename: 'faceted-jquery.min.js',
        },
        externals: {
            jquery: 'jQuery',
        },
    },
    {
        entry: './resources/view.js',
        // optimization: {
        //     minimize: false
        // },
        output: {
            path: path.resolve(__dirname, 'eea/facetednavigation/browser/static'),
            filename: 'faceted-view.min.js',
        },
    },
    {
        entry: './resources/edit.js',
        // optimization: {
        //     minimize: false
        // },
        output: {
            path: path.resolve(__dirname, 'eea/facetednavigation/browser/static'),
            filename: 'faceted-edit.min.js',
        },
    },
];
