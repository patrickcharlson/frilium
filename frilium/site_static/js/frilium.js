$(document).ready(function () {
    $('.action-checkall').change(function () {
        $('input.action-checkbox').prop('checked', this.checked);
    });
});

var BulkActions = function () {
    this.execute = function (endpoint) {
        var selected = $('input.action-checkbox:checked').length;
        var data = {"ids": []};

        // don't do anything if nothing is selected
        if (selected === 0) {
            return false;
        }

        $('input.action-checkbox:checked').each(function (k, v) {
            data.ids.push($(v).val());
        });

        this.confirm(endpoint, data);
        return false;
    };
};