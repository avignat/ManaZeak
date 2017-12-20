/* * * * * * * * * * * * * * * * * * * * * *
 *                                         *
 *  AdminView class                        *
 *                                         *
 *  Handle admin settings                  *
 *                                         *
 * * * * * * * * * * * * * * * * * * * * * */

class AdminView extends View {
    constructor() {

        super();
        this._createUI();
    }

//  --------------------------------  PRIVATE METHODS  --------------------------------  //

    /**
     * method : _createUI (private)
     * class  : AdminView
     * desc   : Build UI elements
     **/
    _createUI() {
        this.ui = {
            container: this.container
        };

        this.ui.container.id = "admin";

        let that = this;
        JSONParsedGetRequest(
            "ajax/getAdminView/",
            function(response) {
                /* response = {
                 *     DONE      : bool
                 *     ERROR_H1  : string
                 *     ERROR_MSG : string
                 * } */
                if (response.DONE) {
                    that.ui.dropLabel            = document.createElement("P");
                    that.ui.dropButton           = document.createElement("BUTTON");

                    that.ui.dropLabel.innerHTML  = "Drop the database";
                    that.ui.dropButton.innerHTML = "DROP";

                    that.ui.container.appendChild(that.ui.dropLabel);
                    that.ui.container.appendChild(that.ui.dropButton);

                    that.ui.dropButton.addEventListener("click", that._requestDrop.bind(that));
                }
            }
        );
    }


    /**
     * method : _requestDrop (private)
     * class  : AdminView
     * desc   : Send a drop db request to the server
     **/
    _requestDrop() {
        JSONParsedGetRequest(
            "ajax/ZNCcuoa8kJL8z6xgNZKnWmMfahHf9j6w6Fi3HFc",
            function(response) {
                /* response = {
                 *     DONE      : bool
                 *     ERROR_H1  : string
                 *     ERROR_MSG : string
                 * } */
                if (!response.DONE) {
                    new Notification("ERROR", response.ERROR_H1, response.ERROR_MSG);
                }

                else {
                    // TODO : refresh UI
                }
            }
        );
    }

}
