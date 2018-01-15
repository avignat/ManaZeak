/* * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                 *
 *  UserMenu class                                 *
 *                                                 *
 *  Handle the user's menu                         *
 *                                                 *
 * * * * * * * * * * * * * * * * * * * * * * * * * */

class UserMenu {
    constructor(container) {

        this.ui = {
            container: document.createElement("DIV"),
            img:       document.createElement("IMG")
        };
        this.menu      = document.createElement("DIV");
        this.menu.id   = "menu";
        this.menuEntry = {
            logout:   null,
            stats:    null,
            settings: null
        };
        this.outside   = document.body;
        this.isVisible = false;

        this._createUI(container);
    }

//  --------------------------------  PRIVATE METHODS  --------------------------------  //

    /**
     * method : _clickOutside (private)
     * class  : UserMenu
     * desc   : On click outside UserMenu
     **/
    _clickOutside(event) {
        if (!document.getElementById("userExpander").contains(event.target) && !document.getElementById("menu").contains(event.target)) {
            removeVisibilityLock(this.menu);
        }
    }


    /**
     * method : _createUI (private)
     * class  : UserMenu
     * desc   : Build UI Elements
     **/
    _createUI(container) {
        this.ui.container.id              = "userExpander";
        this.ui.img.src                   = "/static/img/utils/user.svg";

        this.ui.container.appendChild(this.ui.img);

        this.menuEntry.logout               = document.createElement("DIV");
        this.menuEntry.stats                = document.createElement("DIV");
        this.menuEntry.settings             = document.createElement("DIV");
        this.menuEntry.inviteCode           = document.createElement("DIV");
        this.menuEntry.logout.className     = "menuEntry";
        this.menuEntry.stats.className      = "menuEntry";
        this.menuEntry.settings.className   = "menuEntry";
        this.menuEntry.inviteCode.className = "menuEntry";
        this.menuEntry.logout.innerHTML     = "Log out";
        this.menuEntry.stats.innerHTML      = "Stats";
        this.menuEntry.settings.innerHTML   = "Settings";
        this.menuEntry.inviteCode.innerHTML = "Invite Code";

        let that = this;
        window.app.user.updateIsAdmin(function(is) {
            if (is) {
                that.menuEntry.admin = document.createElement("DIV");
                that.menuEntry.admin.className = "menuEntry";
                that.menuEntry.admin.innerHTML = "Admin";
                that.menuEntry.admin.addEventListener("click", that._getAdmin.bind(that));

                that.menu.appendChild(that.menuEntry.admin);
            }

            that.menu.appendChild(that.menuEntry.inviteCode);
            that.menu.appendChild(that.menuEntry.settings);
            that.menu.appendChild(that.menuEntry.stats);
            that.menu.appendChild(that.menuEntry.logout);

        });

        this.ui.container.appendChild(this.menu);
        container.appendChild(this.ui.container);

        this._eventListener();
    }


    _displayInviteCode() {
        let modal = new Modal("inviteCode", null);
        modal.open();
    }


    /**
     * method : _eventListener (private)
     * class  : UserMenu
     * desc   : UserMenu event listeners
     **/
    _eventListener() {
        let that = this;
        this.ui.img.addEventListener("click", function() {
            that._toggleVisibilityLock();
        });
        this.menuEntry.logout.addEventListener("click", this._logOut.bind(this));
        this.menuEntry.stats.addEventListener("click", this._getStats.bind(this));
        this.menuEntry.settings.addEventListener("click", this._getSettings.bind(this));
        this.menuEntry.inviteCode.addEventListener("click", this._displayInviteCode.bind(this));
        this.outside.addEventListener("click", this._clickOutside.bind(this), false);
    }



    /**
     * method : _getAdmin (private)
     * class  : UserMenu
     * desc   : request Admin View
     **/
    _getAdmin() {
        removeVisibilityLock(this.menu);
        window.app.topBar.unSelectAll();
        window.app.showAppView('mzk_admin');
    }


    /**
     * method : _getAdmin (private)
     * class  : UserMenu
     * desc   : request Admin View
     **/
    _getSettings() {
        removeVisibilityLock(this.menu);
        window.app.topBar.unSelectAll();
        window.app.showAppView('mzk_settings');
    }


    /**
     * method : _getStats (private)
     * class  : UserMenu
     * desc   : request Stats View
     **/
    _getStats() {
        removeVisibilityLock(this.menu);
        window.app.topBar.unSelectAll();
        window.app.showAppView('mzk_stats');
    }


    /**
     * method : _logOut (private)
     * class  : UserMenu
     * desc   : request Log Out
     **/
    _logOut() {
        window.app.logOut();
    }


    /**
     * method : _toggleVisibilityLock (private)
     * class  : UserMenu
     * desc   : Toggle UserMenu visibility
     **/
    _toggleVisibilityLock() {
        if (!this.isVisible) {
            this.isVisible = !this.isVisible;
            addVisibilityLock(this.menu);
        }

        else {
            this.isVisible = !this.isVisible;
            removeVisibilityLock(this.menu);
        }
    }

}
