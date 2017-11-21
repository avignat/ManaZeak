/* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                                                     *
 *  ListView class - classical list view                                               *
 *                                                                                     *
 * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
var ListView = function(data) {

    this.listView = null;
    this.entries = [];
    this.entriesSelected = {};
    this.dblClick = false;

    this.contextMenu = new NewContextMenu();

    this.header = {
        container: null,
        duration:  null,
        title:     null,
        artist:    null,
        composer:  null,
        performer: null,
        album:     null,
        genre:     null,
        bitRate:   null,
        year:      null
    };

    this.sort = {
        isDurationAsc:  false,
        isTitleAsc:     false,
        isArtistAsc:    false,
        isComposerAsc:  false,
        isPerformerAsc: false,
        isAlbumAsc:     false,
        isGenreAsc:     false,
        isBitRateAsc:   false,
        isYearAsc:      false
    };

    View.call(this, data);

};

ListView.prototype = {

    getDataFromPlaylist: function(playlist) {
        return playlist.tracks;
    },

    _init: function(data) {
        this.listView = document.createElement("DIV");
        this.listView.id ="listView";

        this.initHeader();
        this.addEntries(data);
        this.container.appendChild(this.header.container);
        this.container.appendChild(this.listView);
    },


    initHeader: function() {
        this.header.container = document.createElement("DIV");
        this.header.container.className = "columnHeader";

        this.header.duration  = document.createElement("div");
        this.header.title     = document.createElement("div");
        this.header.artist    = document.createElement("div");
        this.header.composer  = document.createElement("div");
        this.header.performer = document.createElement("div");
        this.header.album     = document.createElement("div");
        this.header.genre     = document.createElement("div");
        this.header.bitRate   = document.createElement("div");
        this.header.year      = document.createElement("div");

        this.header.duration.className    = "col-duration";
        this.header.title.className       = "col-title";
        this.header.artist.className      = "col-artist";
        this.header.composer.className    = "col-composer";
        this.header.performer.className   = "col-performer";
        this.header.album.className       = "col-album";
        this.header.genre.className       = "col-genre";
        this.header.bitRate.className     = "col-bitRate";
        this.header.year.className        = "col-year";

        this.header.duration.innerHTML    = "Duration";
        this.header.title.innerHTML       = "Title";
        this.header.artist.innerHTML      = "Artist";
        this.header.composer.innerHTML    = "Composer";
        this.header.performer.innerHTML   = "Performer";
        this.header.album.innerHTML       = "Album";
        this.header.genre.innerHTML       = "Genre";
        this.header.bitRate.innerHTML     = "BitRate";
        this.header.year.innerHTML        = "Year";

        this.header.container.appendChild(this.header.duration);
        this.header.container.appendChild(this.header.title);
        this.header.container.appendChild(this.header.artist);
        this.header.container.appendChild(this.header.composer);
        this.header.container.appendChild(this.header.performer);
        this.header.container.appendChild(this.header.album);
        this.header.container.appendChild(this.header.genre);
        this.header.container.appendChild(this.header.bitRate);
        this.header.container.appendChild(this.header.year);

        //document.getElementById("mainContainer").appendChild(this.header.container);
    },

    addEntries: function(tracks) {
        for (var i = 0; i < tracks.length ;++i)
            this.entries.push(new ListViewEntry(tracks[i], this.listView, i));
    },


    sortBy: function(argument, ascending) {
        this.entries.sort(sortObjectArrayBy(argument, ascending));
    },


    viewClicked: function(event) {
        var that = this;
        var target = event.target;

        if (target === this.listView)
            return true;
        while(target.parentNode !== this.listView) {
            target = target.parentNode;
        }

        var id = target.dataset.listViewID;

        if (this.dblClick) {
            window.app.changeTrack(this.entries[id].track);
            return;
        }
        this.dblClick = true;
        window.setTimeout(function() { that.dblClick = false; }, 400);

        var newState = !this.entriesSelected[id];

        if (!event.ctrlKey && newState === true) { this.unSelectAll(); }

        this.entriesSelected[id] = newState;
        this.entries[id].setIsSelected(newState);
    },


    unSelectAll: function() {
        this.entriesSelected = {};
        for (var i = 0; i < this.entries.length ;++i)
            if (this.entries[i].getIsSelected())
                this.entries[i].setIsSelected(false);
    },


    _eventListener: function() {
        var that = this;

        //this.listView.oncontextmenu = this.listView.oncontextmenu = function() { return false; };
        this.listView.addEventListener("click", this.viewClicked.bind(this));

        // Sorting listeners
        this.header.duration.addEventListener("click", function() {
            that.sort.isDurationAsc = !that.sort.isDurationAsc;
            that.sortBy("duration", that.sort.isDurationAsc);
        });
        this.header.title.addEventListener("click", function() {
            that.sort.isTitleAsc = !that.sort.isTitleAsc;
            that.sortBy("title", that.sort.isTitleAsc);
        });
        this.header.artist.addEventListener("click", function() {
            that.sort.isArtistAsc = !that.sort.isArtistAsc;
            that.sortBy("artist", that.sort.isArtistAsc);
        });
        this.header.composer.addEventListener("click", function() {
            that.sort.isComposerAsc = !that.sort.isComposerAsc;
            that.sortBy("composer", that.sort.isComposerAsc);
        });
        this.header.performer.addEventListener("click", function() {
            that.sort.isPerformerAsc = !that.sort.isPerformerAsc;
            that.sortBy("performer", that.sort.isPerformerAsc);
        });
        this.header.album.addEventListener("click", function() {
            that.sort.isAlbumAsc = !that.sort.isAlbumAsc;
            that.sortBy("album", that.sort.isAlbumAsc);
        });
        this.header.genre.addEventListener("click", function() {
            that.sort.isGenreAsc = !that.sort.isGenreAsc;
            that.sortBy("genre", that.sort.isGenreAsc);
        });
        this.header.bitRate.addEventListener("click", function() {
            that.sort.isBiteRateAsc = !that.sort.isBiteRateAsc;
            that.sortBy("bitRate", that.sort.isBiteRateAsc);
        });
        this.header.year.addEventListener("click", function() {
            that.sort.isYearAsc = !that.sort.isYearAsc;
            that.sortBy("year", that.sort.isYearAsc);
        });
    }
};

extendClass(View, ListView);