JAZZMIN_SETTINGS = {
    "site_title": " Admin",
    "site_header": " Admin",
    "site_brand": ".com",
    
    
    "site_logo": "./logos/icon-2.png",  
    "login_logo": "./logos/logos2.png",   
    "login_logo_dark": "./logos/logos2.png",  
    "site_icon": './logos/icon-2.png',  
    "user_avatar": './logos/icon-2.png',   
    
    "site_logo_classes": " shadow-none d-flex justify-content-center  ",   
    "login_logo_classes": "shadow-none w-100 ",   
    "login_logo_dark_classes": "shadow-none  w-100",   
    
    
    "welcome_sign": "Welcome to the ",
    "copyright": ".com",
    "search_model": "auth.User",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home",  "url": "admin:index", "permissions": ["is_admin"]},
        {"model": "auth.User"},
        {"app": "APP"},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
}

JAZZMIN_SETTINGS["show_ui_builder"] = True

