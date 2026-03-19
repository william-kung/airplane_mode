frappe.listview_settings["Airport Rental Income Tracking"] = {
    formatters: {
        period_start(value, df, doc) {
            if (!value) return ""
            if (doc.status === "Received") return ""
        
            const d = moment(value)
            const now = moment()
            const color = d < now ? "red" : "green"

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
    add_fields: ['status'],
    has_indicator_for_draft: true,
    has_indicator_for_cancelled: true,
    get_indicator: function (doc) {
        const status = doc.status || "Pending"
        const status_map = {
            "Pending": "orange",
            "Overdue": "red",
            "Received": "gray",           
        };
        const label = `${status}`;
        const color = status_map[status] || "gray";
        return [label, color, `status,=,${status}`];
    },
}