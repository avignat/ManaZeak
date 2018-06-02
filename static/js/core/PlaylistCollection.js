/* * * * * * * * * * * * * * * * * * * * * * * * * *
 *                                                 *
 *  PlaylistCollection class                       *
 *                                                 *
 *  A class to handle storing the playlists        *
 *                                                 *
 * * * * * * * * * * * * * * * * * * * * * * * * * */

import MzkObject from './MzkObject.js'

class PlaylistCollection extends MzkObject {

    constructor() {

        super();

        if (window.debug) {
            console.log('  PlaylistCollection construction');
        }

        this.bank = {};
        this.size = 0;
    }

//  --------------------------------  PUBLIC METHODS  ---------------------------------  //

    /**
     * method : add (public)
     * class  : PlaylistCollection
     * desc   : Add a playlist to the collection
     * arg    : {object} playlist
     **/
    add(playlist) {
        if (window.debug) {
            console.log('  PlaylistCollection : add call');
        }

        if (this.get(playlist.id) == null) {
            this.bank[playlist.id] = playlist;
            ++this.size;
            return true;
        }

        else {
            return false;
        }
    }


    /**
     * method : remove(public)
     * class  : PlaylistCollection
     * desc   : Remove a playlist from the collection
     * arg    : {inter} playlistID
     **/
    remove(playlistID) {
        if (window.debug) {
            console.log('  PlaylistCollection : remove call');
        }


        if (this.get(playlistID) != null) {
            delete this.bank[playlistID];
            --this.size;
            return true;
        }

        else {
            return false;
        }
    }


    /**
     * method : rename(public)
     * class  : PlaylistCollection
     * desc   : Rename a playlist from the collection
     * arg    : {inter} playlistID
     *          {string} name
     **/
    rename(playlistID, name) {
        if (window.debug) {
            console.log('  PlaylistCollection : rename call');
        }


        if (this.get(playlistID) != null) {
            this.bank[playlistID].setName(name);
            return true;
        }

        else {
            return false;
        }
    }


    /**
     * method : clear(public)
     * class  : PlaylistCollection
     * desc   : Clear the collection
     **/
    clear() {
        if (window.debug) {
            console.log('  PlaylistCollection : clear call');
        }

        this.bank = {};
        this.size = 0;
    }


    /**
     * method : forEach(public)
     * class  : PlaylistCollection
     * desc   : Call a function on every playlist
     * arg    : {function} callback
     * arg    : {boolean} includeDefault - whether to call on the default playlist
     **/
    forEach(callback, includeDefault) {
        if (window.debug) {
            console.log('  PlaylistCollection : forEach call');
        }


        for (let i in this.bank) {
            if (includeDefault != false || this.bank[i] != this.getDefault()) {
                callback.call(this.bank[i]);
            }
        }
    }


    /**
     * method : filter(public)
     * class  : PlaylistCollection
     * desc   : return all of the playlists that satisfy the function
     * arg    : {function} filterFct
     **/
    filter(filterFct) {
        if (window.debug) {
            console.log('  PlaylistCollection : filter call');
        }


        let result = new Array(this.size);
        let j      = 0;
        for (let i in this.bank) {
            if (filterFct.call(this.bank[i]) == true) {
                result[j] = this.bank[i];
                ++j;
            }
        }

        result.length = j;
        return result;
    }


    /**
     * method : get(public)
     * class  : PlaylistCollection
     * desc   : Get a playlist from the collection
     * arg    : {integer} playlistID
     **/
    get(playlistID) {
        if (window.debug) {
            console.log('  PlaylistCollection : get call');
        }


        return this.bank[playlistID];
    }


    /**
     * method : getDefault(public)
     * class  : PlaylistCollection
     * desc   : Get the default playlist from the collection
     **/
    getDefault() {
        if (window.debug) {
            console.log('  PlaylistCollection : getDefault call');
        }


        for (let i in this.bank) {
            return this.bank[i];
        }

        return null;
    }

}

export default PlaylistCollection