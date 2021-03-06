import ContextMenu from '../../utils/feedback/ContextMenu.js';
'use strict';


class ViewSwitcher extends ContextMenu {
  constructor(options) {
    super(options);

    this._views = {
      track: {},
      album: {}
    };
  }

  setActions(doc) {
    const changeView = (newView) => {
      mzk.changeActiveView(newView);
    };

    this._views.track = doc.getElementsByClassName('track-view')[0];
    this._views.album = doc.getElementsByClassName('album-view')[0];

    this._views.track.addEventListener('click', () => {
      changeView(this._views.track.dataset.view);
    });

    this._views.album.addEventListener('click', () => {
      changeView(this._views.album.dataset.view);
    });
  }
}

export default ViewSwitcher;
