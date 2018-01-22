/* * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                 *
 *  TopBar class                                   *
 *                                                 *
 *  Handle the whole topBar and its components     *
 *                                                 *
 * * * * * * * * * * * * * * * * * * * * * * * * * */

class TopBar extends MzkObject {
    constructor() {
        super();
        this._createUI();
        this._eventListener();
        this.partyMode     = new PartyMode(this.topBar);
        this.wishList      = new WishList(this.topBar);
        this.userMenu      = new UserMenu(this.topBar);
        this.collectionBar = new CollectionBar(window.app.playlists, this.playlistBar);
        this.newLibMenu    = null;
    }

//  --------------------------------  PUBLIC METHODS  ---------------------------------  //

    /**
     * method : changeMoodbar (public)
     * class  : TopBar
     * desc   : Request the moodbar from a track ID and set it
     * arg    : {int} id - The Track ID
     **/
    changeMoodbar(id) {
        let that = this;
        JSONParsedPostRequest(
            "ajax/getMoodbarByID/",
            JSON.stringify({
                TRACK_ID: id
            }),
            function(response) {
                let error = false;
                renderMoodFile(response.MOOD, that.moodbar, function() { // Callback is here in case of 404 on the moodBar
                    that.resetMoodbar();
                    error = true;
                });

                if (!that.moodbarThumb.isVisible && !error) {
                    that.moodbarThumb.isVisible = true;
                    addVisibilityLock(that.moodbarThumb);
                }
            }

        );
    }


    /**
     * method : resetMoodbar (public)
     * class  : TopBar
     * desc   : Erase moodbar content and hide moodbar thumb
     **/
    resetMoodbar() {
        d3.selectAll('#moodbar svg').remove();
        this.moodbarThumb.isVisible = false;
        removeVisibilityLock(this.moodbarThumb);
    }

//  --------------------------------  PRIVATE METHODS  --------------------------------  //


    /**
     * method : _createUI (private)
     * class  : TopBar
     * desc   : Build UI elements
     **/
    _createUI() {

        this.topBar                      = document.createElement("DIV");
        this.moodbar                     = document.createElement("DIV");
        this.moodbarThumb                = document.createElement("DIV");
        this.playlistBar                 = document.createElement("DIV");

        this.topBar.id                   = "topBar";
        this.moodbar.id                  = "moodbar";
        this.moodbarThumb.id             = "moodbarThumb";
        this.playlistBar.id              = "playlistBar";

        this.topBar.appendChild(this.moodbar);
        this.moodbar.appendChild(this.moodbarThumb);
        this.topBar.appendChild(this.playlistBar);

        this.moodbarThumb.isVisible      = false;
    }


    /**
     * method : _eventListener (private)
     * class  : TopBar
     * desc   : Event handlers
     **/
    _eventListener() {
        var that = this;
        window.app.listen('stopPlayback', function() {
            that.resetMoodbar();
        });
        window.app.listen('changeTrack', function(track) {
            that.changeMoodbar(track.id.track);
        });
    }
//  ------------------------------  GETTERS / SETTERS  --------------------------------  //

    getTopBar() { return this.topBar; }

}
