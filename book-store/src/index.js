import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


class ToggleBooksButton extends React.Component {
    constructor(props) {
      super(props);
      this.state = {isToggleOn: true};
  
      // This binding is necessary to make `this` work in the callback    
      this.handleClick = this.handleClick.bind(this);  
    }
  
    handleClick() {    
        this.setState(prevState => ({      
        isToggleOn: !prevState.isToggleOn    
    }));  
    }

    render() {
      return (
        <button onClick={this.handleClick}>        
            {this.state.isToggleOn ? 'ON' : 'OFF'}
        </button>
      );
    }
  }
class BooksService extends React.Component {

    constructor(props) {
      super(props);

      this.state = {
        error: null,
        isLoaded: false,
        items: null,

        isToggleOn: false
      };


      this.handleClick = this.handleClick.bind(this);  
    }

    
  
    componentDidMount() {
      fetch('http://127.0.0.1:8080/bookcollection/books', { 
        method: 'get', 
        headers: new Headers({
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImJ1ZGVhbnVyYWR1OTlAZ21haWwuY29tIiwiZXhwIjoxNjQzNDU2MzczfQ.5c9ZIjkw-0xvMtImBDIBnh1VSmBI8TDKfYOXvus8dLI', 
            'Content-Type': 'application/json'
         })
      })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.carti
          });
          console.log(result);  
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
    }

    handleClick() {    
        this.setState(prevState => ({      
        isToggleOn: !prevState.isToggleOn    
    }));  
    }
  
    render() {
      const { error, isLoaded, items, isToggleOn } = this.state;

      if (error) {
        return <div>Error: {error.message}</div>;
      } else if (!isLoaded) {
        return <div>Loading...</div>;
      } else {
        return (
          
            
          <div>
            <button onClick={this.handleClick}>        
                {this.state.isToggleOn ? 'Ascunde carti' : 'Afiseaza carti'}
            </button>
            
            {
              isToggleOn && items.map(
                item => (
                            <p>
                                {item.titlu} - {item.editura} - {item.gen_literar}
                            </p>
                        )
              )
            }
          </div>
        );
      }
    }
}

  
  
  // ========================================
  
  ReactDOM.render(
    <BooksService />, document.getElementById('root')
  );
  