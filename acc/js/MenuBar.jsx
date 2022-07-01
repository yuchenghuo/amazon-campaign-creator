import React from 'react';

class MenuBar extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className={'row-container'}>
        <a href='/' className={'child'}>
          Amazon Campaign Creator
        </a>
        {this.props.isLoggedIn ?
        <button style={{fontSize: 32}} id={'logout'} className={'login-text'} onClick={this.props.logOut}>
          Log Out
        </button> :
        <a href='/login/' className={'login-text'}>
          Log In
        </a>}
      </div>
    );
  }
}

export default MenuBar;
