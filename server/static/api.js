// API calling utilities.
window.api = (function(axios, XSRFToken) {
  // XSRF token should be injected from parent template.
  axios.defaults.headers.common['X-XSRFToken'] = XSRFToken;

  var root = '/api/v1';
  var module = {};

  /**
   * Fetch widgets matching search parameters.
   * @param params
   * @returns {Promise}
   */
  module.fetchWidgets = function(params) {
    return axios.get(root + '/widgets/', { params: params });
  };

  /**
   * Fetch all the current widget sizes.
   * @returns {Promise}
   */
  module.fetchWidgetSizes = function() {
    return axios.get(root + '/widgets/sizes/');
  };

  /**
   * Fetch all the current widget finishes.
   * @returns {Promise}
   */
  module.fetchWidgetFinishes = function() {
    return axios.get(root + '/widgets/finishes/');
  };

  /**
   * Fetch all the current widget types.
   * @returns {Promise}
   */
  module.fetchWidgetTypes = function() {
    return axios.get(root + '/widgets/types/');
  };

  /**
   * Fetch all the current widget sizes.
   * @returns {Promise}
   */
  module.createOrder = function() {
    return axios.post(root + '/orders/');
  };

  /**
   * Adds a new wiedget to an order.
   * @param orderID {number}
   * @param widgetID {number}
   * @param widgetSizeID {number}
   * @param widgetFinishID {number}
   * @param amount {number}
   * @returns {Promise}
   */
  module.addOrderWidget = function(
    orderID, widgetID, widgetSizeID, widgetFinishID, amount) {
    return axios.post(root + '/orders/' + orderID + '/widgets/', {
      widget_id: widgetID,
      widget_size_id: widgetSizeID,
      widget_finish_id: widgetFinishID,
      amount: amount
    });
  };

  /**
   * Gets an order by it's ID.
   * @param orderID {number}
   * @returns {Promise}
   */
  module.getOrder = function(orderID) {
    return axios.get(root + '/orders/' + orderID + '/');
  };

  /**
   * Delete an order widget.
   * @param widgetID {number}
   * @returns {Promise}
   */
  module.deleteOrderWidget = function(widgetID) {
    return axios.delete(root + '/orders/widgets/' + widgetID + '/');
  };

  /**
   * Delete an entire order.
   * @param orderID {number}
   * @returns {Promise}
   */
  module.deleteOrder = function(orderID) {
    return axios.delete(root + '/orders/' + orderID + '/');
  };

  return module;
})(axios, window.XSRFToken);