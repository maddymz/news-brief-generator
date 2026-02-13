def tile(icon, label, value):
    return f"""
    <div style="
        background:#f8f9fb;
        border:1px solid #e0e4ea;
        border-radius:12px;
        padding:16px 14px;
        text-align:center;
        min-height:90px;
    ">
        <div style="font-size:11px;color:#888;font-weight:600;
                    text-transform:uppercase;letter-spacing:0.8px;
                    margin-bottom:8px;">{icon} {label}</div>
        <div style="font-size:14px;font-weight:600;color:#1a1a2e;
                    word-wrap:break-word;line-height:1.5;">{value}</div>
    </div>"""
