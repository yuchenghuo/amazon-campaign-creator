import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import {
  createTheme,
  MenuItem,
  ThemeProvider,
  Typography
} from "@mui/material";

class SingleKeyword extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: false,
      biddingStrategy: null,
      adjustments: null,
      enabled: false,
      acosTarget: null,
      asin: null,
      sku: null,
      dailyBudget: null,
      campaignStartDate: null,
      campaignEndDate: null,
      keywords: null,
      defaultBid: null,
      bidAdjustment: null,
      initialKeywordBid: null,
      maxBid: null,
    }
    this.setOpen = this.setOpen.bind(this);
    this.handleClickOpen = this.handleClickOpen.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  setOpen(open) {
    this.setState({ open });
  }

  handleClickOpen() {
    this.setOpen(true);
  };

  handleClose() {
    this.setOpen(false);
  };

  handleSubmit() {
    this.setState({
      open: false,
      biddingStrategy: null,
      adjustments: null,
      enabled: false,
      acosTarget: null,
      asin: null,
      sku: null,
      dailyBudget: null,
      campaignStartDate: null,
      campaignEndDate: null,
      keywords: null,
      defaultBid: null,
      bidAdjustment: null,
      initialKeywordBid: null,
      maxBid: null,
    });
    this.handleClose();
    this.props.onSubmit(this.state);
  }

  render() {
    const theme = createTheme({
      palette: {
        primary: {
          main: '#778A35',
        }
      },
      overrides: {
        MuiInputLabel: {
          color:'black',
          fontSize: 13,
          fontFamily: 'Anek Latin, sans-serif',
        },
      }
    });

    return (
      <div>
        <button className={"campaign-theme"} onClick={this.handleClickOpen}>Single Keyword</button>
        <Dialog open={this.state.open} onClose={this.handleClose}>
          <DialogTitle>
            <Typography style={{fontFamily: 'Anek Latin, sans-serif', fontSize: 24}}>
              Single Keyword Campaign
            </Typography>
          </DialogTitle>
          <DialogContent style={{ marginBottom: 0 }}>
            <DialogContentText>
              <p style={{fontFamily: 'Anek Latin, sans-serif', fontSize: 18, fontWeight: 900, marginBottom: 2}}>
                To create a single keyword campaign, please fill out the following form.
              </p>
            </DialogContentText>
            <ThemeProvider theme={theme}>
              <TextField
                autoFocus
                margin="dense"
                label="SKU"
                type="text"
                fullWidth
                onChange={(e) => this.setState({sku: e.target.value})}
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <TextField
                autoFocus
                margin="dense"
                label="ASIN"
                type="text"
                fullWidth
                onChange={(e) => this.setState({asin: e.target.value})}
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <TextField
                margin="dense"
                label="Daily Budget"
                type="number"
                fullWidth
                onChange={(e) => this.setState({dailyBudget: e.target.value})}
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <TextField
                margin="dense"
                label="ACOSTARGET"
                type="text"
                onChange={(e) => this.setState({acosTarget: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <TextField
                margin="dense"
                label="Campaign Start Date"
                type="date"
                onChange={(e) => this.setState({campaignStartDate: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 }, shrink: true  }}
              />
              <TextField
                margin="dense"
                label="Campaign End Date"
                type="date"
                onChange={(e) => this.setState({campaignEndDate: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 }, shrink: true }}
              />
              <TextField
                margin="dense"
                label="Keywords"
                type="text"
                onChange={(e) => this.setState({keywords: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <div style={{display: "flex", flexDirection: "row", marginBottom: 0}}>
                <TextField
                  margin="dense"
                  label="Enabled"
                  type="checkbox"
                  variant="outlined"
                  defaultChecked={false}
                  onChange={(e) => this.setState({enabled: e.target.checked})}
                  style={{ width: 175 }}
                  inputProps={{ style: { margin: 70, minHeight: 53, maxHeight: 53 } }}
                  InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 }, shrink: true }}
                />
                <div style={{ margin: 0, maxWidth: 300 }}>
                  <TextField
                    margin="dense"
                    label="Bidding Strategy"
                    select
                    value={this.state.biddingStrategy}
                    onChange={(e) => this.setState({ biddingStrategy: e.target.value })}
                    fullWidth
                    variant="outlined"
                    style={{ width: 365, marginLeft: 10 }}
                    inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                    InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                  >
                    <MenuItem value={null}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>

                      </Typography>
                    </MenuItem>
                    <MenuItem value={"legacyForSales"}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                        Dynamic bids - down only
                      </Typography>
                    </MenuItem>
                    <MenuItem value={"autoForSales"}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                        Dynamic bids - up and down
                      </Typography>
                    </MenuItem>
                    <MenuItem value={"manual"}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                        Fixed bid
                      </Typography>
                    </MenuItem>
                  </TextField>
                  <TextField
                    margin="dense"
                    label="Adjustment Predicate"
                    select
                    value={this.state.adjustments}
                    onChange={(e) => this.setState({ adjustments: e.target.value })}
                    fullWidth
                    variant="outlined"
                    style={{ width: 365, marginLeft: 10 }}
                    inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18} }}
                    InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18} }}
                  >
                    <MenuItem value={null}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>

                      </Typography>
                    </MenuItem>
                    <MenuItem value={"placementTop"}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                        Top of search (first page)
                      </Typography>
                    </MenuItem>
                    <MenuItem value={"placementProductPage"}>
                      <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                        Product pages
                      </Typography>
                    </MenuItem>
                  </TextField>
                  <TextField
                    margin="dense"
                    label="Percentage"
                    type="number"
                    onChange={(e) => this.setState({percentage: e.target.value})}
                    fullWidth
                    style={{ width: 365, marginLeft: 10 }}
                    variant="outlined"
                    inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif' } }}
                    InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif' } }}
                  />
                </div>
              </div>
              <TextField
                margin="dense"
                label="Default Bid"
                type="number"
                onChange={(e) => this.setState({defaultBid: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <TextField
                margin="dense"
                label="Inital Keyword Bid"
                select
                value={this.state.initialKeywordBid}
                onChange={(e) => this.setState({ initialKeywordBid: e.target.value })}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              >
                <MenuItem value={"default"}>
                  <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                    Default Bid
                  </Typography>
                </MenuItem>
                <MenuItem value={"suggested"}>
                  <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                    Suggested Bid
                  </Typography>
                </MenuItem>
                <MenuItem value={"lower"}>
                  <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                    Suggested Lowest Bid
                  </Typography>
                </MenuItem>
                <MenuItem value={"upper"}>
                  <Typography style={{fontFamily: 'Anek Latin, sans-serif'}}>
                    Suggested Highest Bid
                  </Typography>
                </MenuItem>
              </TextField>
              <TextField
                margin="dense"
                label="Bid Adjustment (%)"
                type="number"
                onChange={(e) => this.setState({bidAdjustment: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
              <TextField
                margin="dense"
                label="Max Bid"
                type="number"
                onChange={(e) => this.setState({maxBid: e.target.value})}
                fullWidth
                variant="outlined"
                inputProps={{ style: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
                InputLabelProps={{ sx: { fontFamily: 'Anek Latin, sans-serif', fontSize: 18 } }}
              />
            </ThemeProvider>
          </DialogContent>
          <DialogActions style={{ marginTop: 0 }}>
            <button className={'form-button'} onClick={this.handleClose}>Cancel</button>
            <button className={'form-button'} onClick={this.handleSubmit}>Confirm</button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

export default SingleKeyword;
