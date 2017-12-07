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

  module.createOrder = function() {
    return axios.post(root + '/orders/');
  };

  module.addOrderWidget = function(orderID, widgetID, widgetSizeID, widgetFinishID, amount) {
    return axios.post(root + '/orders/' + orderID + '/widgets/', {
      widget_id: widgetID,
      widget_size_id: widgetSizeID,
      widget_finish_id: widgetFinishID,
      amount: amount,
    });
  };

  module.getOrder = function(orderID) {
    return axios.get(root + '/orders/' + orderID + '/');
  };

  module.deleteOrderWidget = function(widgetID) {
    return axios.delete(root + '/orders/widgets/' + widgetID + '/');
  };

  module.deleteOrder = function(orderID) {
    return axios.delete(root + '/orders/' + orderID + '/');
  };

  return module;
})(axios, window.XSRFToken);