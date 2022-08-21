import * as React from "react";
import "./App.css";
import * as request from "./request";
import FlashMessage from "react-flash-message"
import axios from "axios";

function App() {
  const [companies, setCompanies] = React.useState();
  const [cleaners, setCleaners] = React.useState();
  const [status, setStatus] = React.useState();

  const [client, setClient] = React.useState()
  const [date, setDate] = React.useState();
  const [start,setStart] = React.useState();
  const [end, setEnd] = React.useState();
  const [msg,setMsg] = React.useState(false)
  


  const handleCleanerList = (event) => {
    request.getCleanersInCompany(event.target.value).then((result) => {
      setCleaners(result);
    });
  };


  const sumbitRequest = (e)=>{
    
    e.preventDefault();
    setMsg(!msg)
    let t = document.getElementById("exampleInput125") //getting the cleaner name
    let cleaner = t.options[t.selectedIndex].text
    
    axios.post("http://127.0.0.1:3001/setAppt", 
        {client,cleaner,start,end,date}
        ).then(d=>console.log(d))
        .catch(er=>console.log(er))
    
    //set the fields back to empty after form submit
    setClient("")
    setDate("")
    setStart("")
    setEnd("")
    setMsg(!msg)
    
  }

  const handleStatus = (event) => {
    setStatus(event.target.value);
  };

  const disableDate = ()=>{
    let dd,mm,yyyy;
    let today = new Date();
    dd = today.getDate()
    mm = today.getMonth()+1
    yyyy = today.getFullYear();

    if(parseInt(mm)<10)
      return `${yyyy}-0${mm}-${dd}` 
    else 
      return `${yyyy}-${mm}-${dd}`
      
  }

  React.useEffect(() => {
    // Update the document title using the browser API
    async function fetchData() {
      const result = await request.getAllCompanies();
      setCompanies(result);
    }
    fetchData();
  }, []);
  React.useEffect(()=>{
    console.log("booking confirmed")
    
  },[msg])
  return (
    <div className="w-6/12 mx-auto bg-gray-200 rounded-xl shadow border p-8 m-10">
      <h1 className="text-3xl text-gray-700 font-bold mb-5">
        Request a cleaner
      </h1>
      <div className="block p-6 rounded-lg shadow-lg bg-white w-full">
        <form onSubmit={sumbitRequest}>
          <div className="grid grid-cols-2 gap-4">
            <div className="form-group mb-6">
              <input
                type="text"
                className="form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                id="exampleInput123"
                aria-describedby="emailHelp123"
                placeholder="Client Email Address"
                value={client}
                name='client'
                onChange = {(e)=>setClient(e.target.value)}
                required
              />
            </div>
            <div className="form-group mb-6">
              <select
                className="form-control
                                      block
                                      w-full
                                      px-3
                                      py-1.5
                                      text-base
                                      font-normal
                                      text-gray-700
                                      bg-white bg-clip-padding
                                      border border-solid border-gray-300
                                      rounded
                                      transition
                                      ease-in-out
                                      m-0
                                      focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                id="exampleInput124"
                aria-describedby="emailHelp124"
                placeholder="Select Company"
                onChange={handleCleanerList}
                required
              >
                {companies ? (
                  companies.map(({ id, name }) => (
                    <option key={id} value={id}>
                      {name}
                    </option>
                  ))
                ) : (
                  <option disabled={true}>Select Company</option>
                )}
              </select>
            </div>
          </div>
          <div className="form-group mb-6">
            <select
              className="form-control block
                                w-full
                                px-3
                                py-1.5
                                text-base
                                font-normal
                                text-gray-700
                                bg-white bg-clip-padding
                                border border-solid border-gray-300
                                rounded
                                transition
                                ease-in-out
                                m-0
                                focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
              id="exampleInput125"
              onChange={handleStatus}
              onClick={handleStatus}
              
              required
            >
              <option disabled={true} value={""}>
                {" "}
                Select cleaner{" "}
              </option>
              {cleaners
                ? cleaners.map(
                    ({ id, name, email_address, availability_status }) => (
                      <option key={id} value={availability_status}>
                        {name}: {email_address}
                      </option>
                    )
                  )
                : ""}
            </select>
          </div>
          <div className="form-group mb-6">
            <div className="flex justify-between border-b">
              {status ? (
                <h4 className="font-bold">Status: {status}</h4>
              ) : (
                <h4 className="font-bold">...</h4>
              )}
            </div>
            <div className="py-3">
              Select Date
              <input
                type="date"
                //min={"2022-08-24"}
                value={date}
                min={disableDate()}
                required
                onChange = {(e)=>{setDate(e.target.value)}}
                className="form-control block
                                    w-full
                                    px-3
                                    py-1.5
                                    text-base
                                    font-normal
                                    text-gray-700
                                    bg-white bg-clip-padding
                                    border border-solid border-gray-300
                                    rounded
                                    transition
                                    ease-in-out
                                    m-0
                                    focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                placeholder="Select Date"
                name="date"
              />
            </div>
            <div className="grid grid-cols-2 gap-4 pt-3">
              <div className="text-sm">Start Hours</div>
              <div className="text-sm">End Hours</div>
              <div className="">
                <input
                  type="time"
                  value={start}
                  required
                  onChange = {(e)=>setStart(e.target.value)}
                  className="form-control block
                                        w-full
                                        px-3
                                        py-1.5
                                        text-base
                                        font-normal
                                        text-gray-700
                                        bg-white bg-clip-padding
                                        border border-solid border-gray-300
                                        rounded
                                        transition
                                        ease-in-out
                                        m-0
                                        focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                  placeholder="Select"
                />
              </div>
              <div className="">
                <input
                  type="time"
                  value = {end}
                  required
                  onChange = {(e)=>setEnd(e.target.value)}
                  className="form-control block
                                        w-full
                                        px-3
                                        py-1.5
                                        text-base
                                        font-normal
                                        text-gray-700
                                        bg-white bg-clip-padding
                                        border border-solid border-gray-300
                                        rounded
                                        transition
                                        ease-in-out
                                        m-0
                                        focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
                  placeholder="Select"
                />
              </div>
            </div>
          </div>
          {/*TODO: Handle submit button*/}
          <button
            disabled={status === "Not available"}
            type="submit"
            className="
                w-full
                px-6
                py-2.5
                bg-blue-600
                text-white
                font-medium
                text-xs
                leading-tight
                uppercase
                rounded
                shadow-md
                hover:bg-blue-700 hover:shadow-lg
                focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0
                active:bg-blue-800 active:shadow-lg
                transition
                duration-150
                ease-in-out"
          >
            Book Cleaner
          </button>
        </form>
        <div>

        </div>
        <div className="message" style={{display:"none"}}>
          {msg && 
              <FlashMessage duration={5000} persistOnHover={true}>
              <p style={{color:"green"}}>Your booking has been confirmed. Check your email.</p>
            </FlashMessage>
            
            }
        </div>
      </div>
    </div>
  );
}

export default App;
