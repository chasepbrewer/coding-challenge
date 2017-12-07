(function(Vue, api, _) {
  // Vue instance for the index page.
  new Vue({
    el: '#index',
    delimiters: ['${', '}'],
    data: {
      order: undefined,
      size: undefined,
      finish: undefined,
      type: undefined,
      sizes: [],
      types: [],
      finishes: [],
      selectedSizes: {},
      selectedFinishes: {},
      widgets: []
    },
    created: function() {
      this.getWidgets();
      this.getWidgetSizes();
      this.getWidgetFinishes();
      this.getWidgetTypes();
    },
    methods: {
      /** Populates the current instance with widgets matching parameters. */
      getWidgets: function() {
        var self = this;
        var params = {
          size: this.size,
          type: this.type,
          finish: this.finish
        };

        api.fetchWidgets(params).then(function(response) {
          self.widgets = response.data.results;
          self.selectedSizes = {};
          self.selectedFinishes = {};

          _.forEach(self.widgets, function(widget) {
            self.selectedSizes[widget.id] = widget.sizes[0].id;
            self.selectedFinishes[widget.id] = widget.finishes[0].id;
          })
        })
      },

      /** Populates instance with all widget sizes. */
      getWidgetSizes: function() {
        var self = this;

        api.fetchWidgetSizes().then(function(response) {
          self.sizes = response.data.results;
        });
      },

      /** Populates instance with all widget finishes. */
      getWidgetFinishes: function() {
        var self = this;

        api.fetchWidgetFinishes().then(function(response) {
          self.finishes = response.data.results;
        });
      },

      /** Populates instance with all widget types. */
      getWidgetTypes: function() {
        var self = this;

        api.fetchWidgetTypes().then(function(response) {
          self.types = response.data.results;
        });
      },

      /**
       * Adds a widget to the current order.
       * @param widgetID {number}
       * @param widgetSizeID {number}
       * @param widgetFinishID {number}
       * @param amount {number}
       * @returns {Promise}
       */
      addOrderWidget: function(widgetID, widgetSizeID, widgetFinishID, amount) {
        if (!this.order) {
          return this.createOrder(
            widgetID, widgetSizeID, widgetFinishID, amount
          );
        }

        var self = this;

        return api.addOrderWidget(
          this.order.id, widgetID, widgetSizeID, widgetFinishID, amount
        ).then(function() {
          return api.getOrder(self.order.id);
        }).then(function(response) {
          self.order = response.data;
        });
      },

      /**
       * Creates a new order
       * @param widgetID {number}
       * @param widgetSizeID {number}
       * @param widgetFinishID {number}
       * @param amount {number}
       * @returns {Promise}
       */
      createOrder: function(widgetID, widgetSizeID, widgetFinishID, amount) {
        var self = this;

        return api.createOrder().then(function(response) {
          self.order = response.data;

          return self.addOrderWidget(
            widgetID, widgetSizeID, widgetFinishID, amount
          );
        });
      },

      /**
       * Deletes a widget from the current order.
       * @param orderWidgetID {number}
       * @returns {Promise | undefined}
       */
      deleteOrderWidget: function(orderWidgetID) {
        if (!this.order) { return; }

        var self = this;

        return api.deleteOrderWidget(orderWidgetID).then(function() {
          return api.getOrder(self.order.id);
        }).then(function(response) {
          // If there are no more widgets left in the order, delete the order.
          if (!response.data.widgets.length) {
            return self.deleteOrder();
          }

          self.order = response.data;
        });
      },

      /** Deletes the current order. */
      deleteOrder: function() {
        if (!this.order) { return; }

        var self = this;

        return api.deleteOrder(this.order.id).then(function() {
          self.order = undefined;
        })
      }
    }
  })
})(Vue, window.api, _);