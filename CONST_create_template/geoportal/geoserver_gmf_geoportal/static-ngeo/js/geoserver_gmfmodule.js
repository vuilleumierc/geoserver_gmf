/**
 * This file provides the "geoserver_gmf" namespace, which is the
 * application's main namespace. And it defines the application's Angular
 * module.
 */

import angular from 'angular';
import {decodeQueryString} from 'ngeo/utils.js';

/**
 * @type {!angular.IModule}
 */
const myModule = angular.module('geoserver_gmf', []);

myModule.config([
  '$compileProvider',
  function ($compileProvider) {
    if (!('debug' in decodeQueryString(window.location.search))) {
      // Disable the debug info
      $compileProvider.debugInfoEnabled(false);
    }
  },
]);

export default myModule;
