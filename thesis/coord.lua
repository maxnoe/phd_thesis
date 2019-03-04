function sph2cart(r, theta, phi)
  local st = math.sin(math.rad(theta))
  local ct = math.cos(math.rad(theta))
  local sp = math.sin(math.rad(phi))
  local cp = math.cos(math.rad(phi))
  local x = r * st * cp;  
  local y = r * st * sp;
  local z = r * ct;
  return {x, y, z}
end


function dot(v1, v2) 
  local sum = 0.0
  for i=1,3 do
    sum = sum + (v1[i] * v2[i])
  end
  return sum
end

function norm(v)
  return math.sqrt(dot(v, v))
end

function normalize(v) 
  local n = norm(v)
  return {v[1] / n, v[2] / n, v[3] / n}
end

function mirror(v, axis) 
  local axis = normalize(axis)  
  local prod = dot(v, axis)
  return {
    2 * prod * axis[1] - v[1],
    2 * prod * axis[2] - v[2],
    2 * prod * axis[3] - v[3]
  }
end


p_az = 160
p_zd = 70
p_r = 0.6

s_az = 155
s_zd = 68
s_r = 0.6

p = sph2cart(p_r, p_zd, p_az)
s = sph2cart(s_r, s_zd, s_az)
m_s = mirror(s, p)

function insert_coord(p)
  tex.sprint("(" .. p[1] .. ", " .. p[2] .. ", " .. p[3] .. ")")
end
