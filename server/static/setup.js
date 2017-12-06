(function(axios) {
  // Sets the XSRF token for any API requests
  axios.defaults.headers.common['X-XSRFToken'] = window.XSRFToken;
})(axios)