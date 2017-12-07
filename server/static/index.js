(function(Vue, api, _) {
  window.indexComponent = new Vue({
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
      widgets: [],
    },
    created: function() {
      this.getWidgets();
      this.getWidgetSizes();
      this.getWidgetFinishes();
      this.getWidgetTypes();
    },
    methods: {
      getWidgets: function() {
        var self = this;
        var params = {
          size: this.size,
          type: this.type,
          finish: this.finish,
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
      getWidgetSizes: function() {
        var self = this;

        api.fetchWidgetSizes().then(function(response) {
          self.sizes = response.data.results;
        });
      },
      getWidgetFinishes: function() {
        var self = this;

        api.fetchWidgetFinishes().then(function(response) {
          self.finishes = response.data.results;
        });
      },
      getWidgetTypes: function() {
        var self = this;

        api.fetchWidgetTypes().then(function(response) {
          self.types = response.data.results;
        });
      },
      changeSize: function(event) {
        this.size = event.target.value;
        this.getWidgets();
      },
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
      createOrder: function(widgetID, widgetSizeID, widgetFinishID, amount) {
        var self = this;

        return api.createOrder().then(function(response) {
          self.order = response.data;

          return self.addOrderWidget(
            widgetID, widgetSizeID, widgetFinishID, amount
          );
        });
      },
      deleteOrderWidget: function(orderWidgetID) {
        if (!this.order) { return; }

        var self = this;

        return api.deleteOrderWidget(this.order.id, orderWidgetID).then(function() {
          return api.getOrder(self.order.id);
        }).then(function(response) {
          if (!response.data.widgets.length) {
            return self.deleteOrder();
          }

          self.order = response.data;
        });
      },
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