import Komunikator from './Komunikator.js';
import Model from '../model/Model.js';
import View from '../view/View.js';
import User from './User.js';
import Notification from "../utils/Notification";
'use strict';


class Mzk {
  /**
   * @summary ManaZeak main controller
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Handle both Model ad View, and animate them accordingly. Host User, Langage and Komunikator also.
   **/
  constructor() {
    this.cookies = {};
    this.komunikator = {};
    this.lang = {};
    this.model = {};
    this.user = {};
    this.view = {};
  }


  //  ----  SESSION INITIALIZATION  ----  //


  /**
   * @method
   * @name start
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init a ManaZeak session depending on user settings in db
   **/
  start() {
    this.cookies = Utils.getCookies(); // Get user cookies

    this._initKomunikator()
      .then(() => {
        return this._initLang();
      })
      .then(() => {
        return this._initUser();
      })
      .then(() => {
        return this._initModel();
      })
      .then(() => {
        return this._initView();
      })
      .then(() => {
        return this._initShortcut();
      })
      .then(() => {
        return this._startApp();
      })
      .catch(() => {
        Errors.raise({
          code: 'FATAL_ERROR',
          frontend: true
        });
      });
  }


  /**
   * @method
   * @name _initKomunikator
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init the Komunikator object (cookies must have been stored before)
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _initKomunikator() {
    return new Promise(resolve => {
      this.komunikator = new Komunikator({
        csrfToken: this.cookies['csrftoken']
      });
      resolve();
    });
  }


  /**
   * @method
   * @name _initUser
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init the User object
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _initUser() {
    return new Promise((resolve, reject) => {
      this.user = new User();
      this.komunikator.get('user/getInformation/')
        .then(userInfo => {
          this.user.setMembers(userInfo);
          resolve();
        })
        .catch(errorCode => {
          Errors.raise({
            code: errorCode,
            frontend: true
          });
          reject();
        });
    });
  }


  /**
   * @method
   * @name _initLang
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init the lang keys and attach them to this
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _initLang() {
    const checkLang = (lang) => { // In case language JSON can not be fetched, we raise a manual notification only.
      if (lang.DONE) {
        this.lang = lang;
      } else {
        Notification.new({
          type: 'error',
          title: 'Unable to load language',
          message: 'Something went wrong, languages settings can not be received.'
        });
      }
    };

    return new Promise(resolve => {
      const options = {
        LANG: (navigator.language || navigator.userLanguage)
      };

      this.komunikator.post('language/', options)
        .then(lang => {
          checkLang(lang);
          resolve();
        }); // Errors can not be catched since language failed loading.
    });
  }


  /**
   * @method
   * @name _initModel
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init the frontend Model
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _initModel() {
    return new Promise(resolve => {
      this.model = new Model();
      resolve();
    });
  }


  /**
   * @method
   * @name _initView
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init the frontend View
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _initView() {
    return new Promise(resolve => {
      this.view = new View();
      resolve();
    });
  }


  /**
   * @method
   * @name _initShortcut
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Init the user shortcuts
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _initShortcut() {
    return new Promise(resolve => {
      this.reloadShortcuts();
      resolve();
    });
  }


  /**
   * @method
   * @name _startApp
   * @private
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Start the UI building (must be called when everything have been safely initialized)
   * @returns {Promise} - A promise that resolve when logic has been executed
   **/
  _startApp() {
    return new Promise((resolve, reject) => {
      this.komunikator.get('playlist/getUserPlaylists/')
        .then(collection => {
          this.model.initCollection(collection)
            .then(playlist => {
              this.view.initPlaylist(playlist);
              resolve();
            })
            .catch(errorKey => {
              Errors.raise({
                code: errorKey,
                frontend: false
              });
              reject();
            });
        })
        .catch(errorKey => {
          Errors.raise({
            code: errorKey,
            frontend: true
          });
          reject();
        });
    });
  }


  //  ----  PLAYBACK METHODS  ----  //


  /**
   * @method
   * @name changeTrack
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Change the played track with the gievn one (using its ID)
   * @param {number} id - The track ID to request to the server
   **/
  changeTrack(id) {
    let durationPlayed = 0;

    if (!isNaN(this.model.getPlayer().getProgress())) {
      durationPlayed = this.model.getPlayer().getProgress();
    }

    const options = {
      TRACK_ID: id,
      LAST_TRACK_PATH: this.model.getPlayer().getSource(),
      TRACK_PERCENTAGE: durationPlayed,
      PREVIOUS: false
    };

    this.komunikator.post('track/getPath/', options)
      .then(track => {
        return this.model.changeTrack(id, track.TRACK_PATH);
      })
      .then(() => {
        this.view.changeTrack(this.model.getActiveTrack());
      });

    // Ci-gît ce petit banc de test, pour le lulz uniquement
    //.then(url => { return this.model.changeTrack('http://static.kevvv.in/sounds/callmemaybe.mp3') })
  }


  /**
   * @method
   * @name togglePlay
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Toggle the playback and update the view
   **/
  togglePlay() {
    if (!this.model.getPlayer().hasSource()) {
      this.changeTrack(this.view.getFirstTrackId());
    } else {
      this.model.togglePlay()
        .then(() => {
          this.view.togglePlay();
        });
    }
  }


  /**
   * @method
   * @name stopPlayback
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Stop the playback and update the view
   **/
  stopPlayback() {
    this.model.stopPlayback()
      .then(() => {
        this.view.stopPlayback();
      });
  }


  //  ----  VOLUME METHODS  ----  //


  /**
   * @method
   * @name mute
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Mute the player
   **/
  mute() {
    this.model.mute();
    this.view.updateVolume();
  }


  /**
   * @method
   * @name unmute
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Un Mute the player
   **/
  unmute() {
    this.model.unmute();
    this.view.updateVolume();
  }


  /**
   * @method
   * @name toggleMute
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Toggle the player's mute state and update the view
   **/
  toggleMute() {
    this.model.toggleMute()
      .then(() => {
        this.view.updateVolume();
      });
  }


  /**
   * @method
   * @name adjustVolume
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Add/Substract a given amount of volume, in range float[-1, 1] and update the view
   **/
  adjustVolume(amount) {
    this.model.adjustVolume(amount)
      .then(() => {
        this.view.updateVolume();
      });
  }


  /**
   * @method
   * @name setVolume
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Add/Substract a given amount of volume, in range float[0, 1] and update the view
   **/
  setVolume(volume) {
    this.model.setVolume(volume)
      .then(() => {
        this.view.updateVolume();
      });
  }


  //  ----  PROGRESS METHODS  ----  //


  /**
   * @method
   * @name adjustProgress
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Adjust the progress percentage from a given amoun in range float[-100,100] and update the view
   **/
  adjustProgress(amount) {
    this.model.adjustProgress(amount)
      .then(() => {
        this.view.updateProgress();
      });
  }


  /**
   * @method
   * @name setProgress
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Set the progress percentage in range float[0,100] and update the view
   **/
  setProgress(progress) {
    this.model.setProgress(progress)
      .then(() => {
        this.view.updateProgress();
      });
  }


  /**
   * @method
   * @name trackEnded
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Triggered when the player reached the end of a track
   **/
  trackEnded() {
    mzk.nextTrackInView();
  }


  /**
   * @method
   * @name changeActiveView
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since November 2018
   * @description Set a new active view to the active playlist
   **/
  changeActiveView(newView) {
    this.model.setActiveView(newView)
      .then(() => {
        this.view.setActiveView(this.model.getCollection().activePlaylist);
      });
  }


  /**
   * @method
   * @name nextTrackInView
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since October 2018
   * @description Change the player track using the next one in the current view
   **/
  nextTrackInView() {
    if (this.model.queue.length > 0) {
      mzk.changeTrack(this.model.getNextFromQueue());
      return;
    }

    const repeatMode = this.model.repeatMode;

    if (repeatMode === 0) {
      if (this.view.isLastTrack()) {
        this.stopPlayback();
      } else {
        mzk.changeTrack(this.view.getNextTrackId());
      }
    } else if (repeatMode === 1) {
      mzk.repeatTrack();
    } else if (repeatMode === 2) {
      mzk.changeTrack(this.view.getNextTrackId());
    } else {
      Errors.raise({
        code: 'NO_NEXT_TRACK',
        frontend: true
      });
    }
  }


  /**
   * @method
   * @name previousTrackInView
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since October 2018
   * @description Change the player track using the previous one in the current view
   **/
  previousTrackInView() {
    mzk.changeTrack(this.view.getPreviousTrackId());
  }


  repeatTrack() {
    this.model.repeatTrack();
    // No need to update the view since the current track didn't changed
  }


  addTrackToQueue(datasetId) {
    const track = this.view.getTrackById(datasetId);

    if (track) {
      this.model.appendToQueue(track.id);
    }
  }


  /**
   * @method
   * @name toggleRepeatMode
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since October 2018
   * @description Change the repeat state to the next one (off, one, all)
   **/
  toggleRepeatMode() {
    this.model.toggleRepeatMode()
      .then((repeatMode) => {
        this.view.setRepeatMode(repeatMode);
      });
  }

  //  ----  SHORTCUTS METHODS  ----  //


  /**
   * @method
   * @name reloadShortcuts
   * @public
   * @memberof Mzk
   * @author Arthur Beaulieu
   * @since September 2018
   * @description Clear registered shortcuts and reload them all from User preferences, when they'll be a thing
   **/
  reloadShortcuts() {
    Shortcut.unregisterAll();

    // Multi keys shortcuts must be declared before simple ones, to respect the trigger ordre

    // Volume control
    Shortcut.register('Ctrl+Shift+ArrowDown', () => {
      this.adjustVolume(-0.25);
    });

    Shortcut.register('Ctrl+Shift+ArrowUp', () => {
      this.adjustVolume(0.25);
    });

    Shortcut.register('Ctrl+ArrowDown', () => {
      this.adjustVolume(-0.1);
    });

    Shortcut.register('Ctrl+ArrowUp', () => {
      this.adjustVolume(0.1);
    });

    Shortcut.register('ArrowDown', () => {
      this.adjustVolume(-0.01);
    });

    Shortcut.register('ArrowUp', () => {
      this.adjustVolume(0.01);
    });

    // Progress control
    Shortcut.register('Ctrl+Shift+ArrowLeft', () => {
      this.adjustProgress(-25);
    });

    Shortcut.register('Ctrl+Shift+ArrowRight', () => {
      this.adjustProgress(25);
    });

    Shortcut.register('Ctrl+ArrowLeft', () => {
      this.adjustProgress(-10);
    });

    Shortcut.register('Ctrl+ArrowRight', () => {
      this.adjustProgress(10);
    });

    Shortcut.register('ArrowLeft', () => {
      this.adjustProgress(-1);
    });

    Shortcut.register('ArrowRight', () => {
      this.adjustProgress(1);
    });

    // Playback control
    Shortcut.register(' ', () => {
      this.togglePlay();
    });
  }


  logOut() {
    this.komunikator.getBinaryResponse('logout/')
      .then(() => {
        location.reload();
      });
  }


  //  ----  GETTERS / SETTERS  ----  //


  getIsMuted() {
    return this.model.getPlayer().getIsMuted();
  }
  getProgress() {
    return this.model.getPlayer().getProgress();
  }
  getVolume() {
    return this.model.getVolume();
  }
}

export default Mzk;
