window.api = (function(axios, XSRFToken) {
  axios.defaults.headers.common['X-XSRFToken'] = XSRFToken;

  var root = '/api/v1';
  var module = {};

  module.fetchWidgets = function(params) {
    return axios.get(root + '/widgets/', { params: params });
  };

  module.fetchWidgetSizes = function() {
    return axios.get(root + '/widgets/sizes/');
  };

  module.fetchWidgetFinishes = function() {
    return axios.get(root + '/widgets/finishes/');
  };

  module.fetchWidgetTypes = function() {
    return axios.get(root + '/widgets/types/');
  };

  return module;
})(axios, window.XSRFToken);