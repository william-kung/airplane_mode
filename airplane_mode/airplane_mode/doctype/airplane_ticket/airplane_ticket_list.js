frappe.listview_settings["Airplane Ticket"] = {
    add_fields: ['status'],
    has_indicator_for_draft: true,
    has_indicator_for_cancelled: true,
    get_indicator: function (doc) {
        const status = doc.status || "Booked"
        const status_map = {
            "Booked": "gray",
            "Checked-In": "purple",
            "Boarded": "green",          
        };
        const label = `${status}`;
        const color = status_map[status] || "gray";
        return [label, color, `status,=,${status}`];
    },
}