goog.provide('app.PreferencesController');
goog.provide('app.preferencesDirective');

goog.require('app');
goog.require('app.Alerts');
goog.require('app.Api');
goog.require('app.Authentication');
goog.require('app.utils');


/**
 * Directive managing the user preferences.
 * @return {angular.Directive} The directive specs.
 * @ngInject
 */
app.preferencesDirective = function() {
  return {
    restrict: 'A',
    scope: true,
    controller: 'appPreferencesController',
    controllerAs: 'prefCtrl',
    bindToController: true
  };
};


app.module.directive('appPreferences', app.preferencesDirective);

/**
 * @param {angular.Scope} $scope Scope.
 * @param {app.Authentication} appAuthentication
 * @param {app.Alerts} appAlerts
 * @param {app.Api} appApi Api service.
 * @param {string} authUrl Base URL of the authentication page.
 * @constructor
 * @ngInject
 * @export
 */
app.PreferencesController = function($scope, appAuthentication, appAlerts,
    appApi, authUrl) {

  /**
   * @type {angular.Scope}
   * @private
   */
  this.scope_ = $scope;

  /**
   * @type {app.Alerts}
   * @private
   */
  this.alerts_ = appAlerts;

  /**
   * @type {app.Api}
   * @private
   */
  this.api_ = appApi;

  if (appAuthentication.isAuthenticated()) {
    this.api_.readPreferences().then(function(data) {
      // TODO
    }.bind(this));
  } else {
    app.utils.redirectToLogin(authUrl);
  }
};


/**
 * @export
 */
app.PreferencesController.prototype.save = function() {
  // TODO
  var modifiedData = {};
  this.api_.updatePreferences(modifiedData).then(function() {
    var msg = this.alerts_.gettext('Update success');
    this.alerts_.addSuccess(msg);
  }.bind(this));
};


app.module.controller('appPreferencesController', app.PreferencesController);
