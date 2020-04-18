const myPost = async (postBody) => {
    const rawResponse = await fetch('https://api.covid19api.com/summary', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(postBody)
    });
    const response = await rawResponse.json();
    console.log(response);
};