import React from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography
} from "@mui/material";

class ProfileSelect extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      profiles: [{'profileId': 0, 'countryCode': 'N/A', 'accountInfo': {'name': 'Please Log In First'}}],
    };
    this.handleChange = this.handleChange.bind(this);
  }

  componentDidMount() {
    fetch('/profiles/')
      .then(response => response.json())
      .then(data => {
        this.setState({
          profiles: data.profiles,
        });
        this.props.onChange(data.profiles[0]);
      })
      .catch(error => console.log(error));
  }

  handleChange(event) {
    this.props.onChange(this.state.profiles.find((profile) => profile.profileId === event.target.value));
  }

  render() {
    const MenuItems = this.state.profiles.map((profile, i) => (
      <MenuItem key={i} value={profile.profileId}>
        <Typography style={{ fontSize: 21, fontFamily: "Anek Latin, sans-serif", height: 30 }}>
          {profile.accountInfo.name} ({profile.countryCode})
        </Typography>
      </MenuItem>
    ));

    return (
      <Box sx={{ width: 400, marginLeft: 12, marginTop: 4 }}>
        <FormControl fullWidth>
          <InputLabel className={"select-box"}>
            <Typography style={{ color: "white", fontSize: 21, fontFamily: "Anek Latin, sans-serif" }}>
              Profile
            </Typography>
          </InputLabel>
          <Select
            value={this.props.profileSelected.profileId}
            label="Profile"
            onChange={this.handleChange}
          >
            {MenuItems}
          </Select>
        </FormControl>
      </Box>
    );
  }
}

export default ProfileSelect;
