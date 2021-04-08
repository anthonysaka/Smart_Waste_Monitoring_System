'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: '"http://localhost:5000/gomibako/internalapi/1.0"',
  SERVER_URL: '"http://localhost:5000"'
})
