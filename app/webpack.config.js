const config = {
    module: {},
};

module.exports = {
    
}

const react = Object.assign({}, config, {
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }
        ]
    }
});

// Return Array of Configurations
module.exports = [
    react
];
