import React from 'react'

const Cards = ({project,key}) => {
    return (
        <div key={key}>
            <div class="card border-light mb-3" style={{maxWidth:"20rem"}}>
  <div class="card-header">Project</div>
  <div class="card-body">
    <h4 class="card-title">{project}</h4>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
  </div>
</div>
        </div>
    )
}

export default Cards
