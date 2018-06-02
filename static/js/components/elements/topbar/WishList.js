/* * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                 *
 *  WishList class                                 *
 *                                                 *
 *  Handle track information and suggests tracks,  *
 *  triggered on hover over a view entry           *
 *                                                 *
 * * * * * * * * * * * * * * * * * * * * * * * * * */
// TODO : add a list of the user's suggestions (link in modal ?)
import Modal from '../../../utils/Modal.js'

class WishList {

    constructor(container) {
        this.LOG = false; // Set to false to locally mute file
        if (window.debug && this.LOG) {
            console.log('      WishList construction');
        }

        this._createUI(container);
        this._eventListener();
    }

//  --------------------------------  PRIVATE METHODS  --------------------------------  //

    /**
     * method : _createUI (private)
     * class  : WishList
     * desc   : Build UI elements
     * arg    : {object} container - The WishList container
     **/
    _createUI(container) {
        if (window.debug && this.LOG) {
            console.log('      WishList : _createUI call');
        }

        this.ui = {
            container: document.createElement("DIV"),
            img:       document.createElement("IMG")
        };

        this.ui.container.className = "mzk-wishes-button";
        this.ui.img.src             = "/static/img/controls/idea.svg";

        this.ui.container.appendChild(this.ui.img);
        container.appendChild(this.ui.container);
    }


    /**
     * method : _eventListener (private)
     * class  : WishList
     * desc   : WishList event listeners
     **/
    _eventListener() {
        if (window.debug && this.LOG) {
            console.log('      WishList : _eventListener call');
        }

        this.ui.img.addEventListener("click", function() {
            let modal = new Modal("newWish");
            modal.open();
        });
    }

}

export default WishList