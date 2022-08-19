import axios from 'axios'


export async function getAllCompanies() {
  try {
    let value = await axios({
      method: "get",
      url: "http://127.0.0.1:3001/companies",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return value.data.resource;
  } catch (error) {
    console.log("error", error);
  }
}

export async function getCleanersInCompany(company_id) {
  try {
    let value = await axios({
      method: "get",
      url: `http://127.0.0.1:3001/users/${company_id}`,
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    return value.data.resource;
  } catch (error) {
    console.log("error", error);
  }
}

