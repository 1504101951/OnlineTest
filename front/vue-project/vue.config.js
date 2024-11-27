const {defineConfig} = require('@vue/cli-service')
const AutoImport = require("unplugin-auto-import/webpack");
const Components = require("unplugin-vue-components/webpack");
const {ElementPlusResolver} = require("unplugin-vue-components/resolvers");
const IconsResolver = require('unplugin-icons/resolver');
const Icons = require('unplugin-icons/webpack');
module.exports = defineConfig({
    lintOnSave: false,
    configureWebpack: {
        plugins: [
            AutoImport({
                resolvers: [ElementPlusResolver(),
                    IconsResolver({
                        prefix: 'Icon',
                    })]
            }),
            Components({
                resolvers: [ElementPlusResolver(),
                    IconsResolver({
                        enabledCollections: ['ep'],
                    })]
            }),
            Icons({
                autoInstall: true,
            }),
        ]
    },
    transpileDependencies: true,
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:3100',
                changeOrigin: true,
                pathRewrite: {
                    ['^' + process.env.VUE_APP_BASE_API]: ''
                }
            }
        },
        allowedHosts:
            [
                'http://localhost:3100'
            ]
    }
});