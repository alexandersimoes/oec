export const activateSearch = searchActive => dispatch => {
  dispatch({type: "ACTIVATE_SEARCH", activate: searchActive});
};
