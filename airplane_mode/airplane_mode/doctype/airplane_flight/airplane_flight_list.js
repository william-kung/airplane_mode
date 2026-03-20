frappe.listview_settings["Airplane Flight"] = {
    add_fields: ['status'],
    has_indicator_for_draft: true,
    has_indicator_for_cancelled: true,
    get_indicator: function (doc) {
        const status = doc.status || "Scheduled"
        const status_map = {
            "Scheduled": "green",
            "Completed": "gray",
            "Cancelled": "red",          
        };
        const label = `${status}`;
        const color = status_map[status] || "gray";
        return [label, color, `status,=,${status}`];
    },
    formatters: {
        date_of_departure(value, df, doc) {
            if (!value) return ""
            const  d = moment(value)
            const now = moment()
            const buffer_before_departure = moment(value).subtract(1, 'days') 
            const is_soon = now.isBetween(buffer_before_departure, d)
            let color
            switch (is_soon) {
                case true:
                    color = "red"
                    break;
                case false:
                    color = d < now ? "gray" : "green"
                    break;
            }

            return `
                <span 
                    class="pill" 
                    style="background-color: var(--bg-${color}); color: var(--text-on-${color}); font-weight: 500;"
                >
                    ${d.fromNow()}
                </span>            
            `
        },
    },
}